from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta


def get_week_bounds(d=None):
    if d is None:
        d = date.today()
    days_since_sunday = (d.weekday() + 1) % 7
    week_start = d - timedelta(days=days_since_sunday)
    week_end   = week_start + timedelta(days=6)
    return week_start, week_end


class Command(BaseCommand):
    help = 'Prepare weekly bio matches for all candidates'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--user-id', type=int, default=None)

    def handle(self, *args, **options):
        from matrimony.models import (
            MaleCandidate, FemaleCandidate,
            CandidateExpectation, BioToken, BioSendLog, WeeklyBioRun,
        )
        dry_run  = options['dry_run']
        user_id  = options.get('user_id')
        week_start, week_end = get_week_bounds()
        week_key  = str(week_start)
        week_label = f"{week_start} முதல் {week_end} வரை"

        # 1. Block if already run this week
        if not dry_run:
            if WeeklyBioRun.objects.filter(week_start=week_start).exists():
                self.stdout.write(self.style.ERROR(
                    f"இந்த வாரம் ({week_label}) ஏற்கனவே இயக்கப்பட்டது."
                ))
                return

        # 2. Delete BioSendLog older than 6 months
        if not dry_run:
            cutoff_month = (date.today() - timedelta(days=180)).strftime('%Y-%m-%d')
            deleted, _ = BioSendLog.objects.filter(month_year__lt=cutoff_month).delete()
            if deleted:
                self.stdout.write(f"{deleted} பழைய பதிவுகள் நீக்கப்பட்டன.")

        self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}வார பயோ தயாரிப்பு — {week_label}")

        male_prepared   = self._prepare_for_gender(MaleCandidate,   FemaleCandidate, 'M', 'F', week_key, dry_run)
        female_prepared = self._prepare_for_gender(FemaleCandidate, MaleCandidate,   'F', 'M', week_key, dry_run)
        total_prepared  = male_prepared + female_prepared

        # 3. Save run log
        if not dry_run:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            run_by = User.objects.filter(pk=user_id).first() if user_id else None
            WeeklyBioRun.objects.create(
                run_by=run_by,
                week_start=week_start,
                week_end=week_end,
                male_processed=MaleCandidate.objects.count(),
                female_processed=FemaleCandidate.objects.count(),
                matches_created=total_prepared,
                notes=f"வார இயக்கம் {week_label}. மொத்தம் {total_prepared} பொருத்தங்கள்.",
            )

        self.stdout.write(self.style.SUCCESS(
            f"{'[DRY RUN] ' if dry_run else ''}மொத்தம் {total_prepared} பொருத்தங்கள் தயார்."
        ))

    def _get_weekly_limit(self, candidate):
        if candidate.premium_type:
            limit = candidate.premium_type.weekly_limit
            return None if limit == 0 else limit
        return 5

    def _prepare_for_gender(self, sender_model, receiver_model,
                             sender_gender, receiver_gender, week_key, dry_run):
        from matrimony.models import CandidateExpectation, BioToken, BioSendLog
        prepared = 0

        for sender in sender_model.objects.select_related('premium_type').all():
            if not sender.whatsapp_number:
                continue

            limit = self._get_weekly_limit(sender)

            # Enforce limit — trim excess pending this week
            if limit is not None:
                all_this_week = BioSendLog.objects.filter(
                    sender_gender=sender_gender, sender_id=sender.pk, month_year=week_key
                ).order_by('prepared_at')
                total_this_week = all_this_week.count()
                if total_this_week > limit:
                    excess_ids = list(
                        all_this_week.filter(status='pending')
                        .order_by('-prepared_at')
                        .values_list('pk', flat=True)[:total_this_week - limit]
                    )
                    BioSendLog.objects.filter(pk__in=excess_ids).delete()

            already_prepared = BioSendLog.objects.filter(
                sender_gender=sender_gender, sender_id=sender.pk, month_year=week_key
            ).count()

            if limit is not None and already_prepared >= limit:
                continue

            remaining = (limit - already_prepared) if limit is not None else 999

            sent_ids = set(BioSendLog.objects.filter(
                sender_gender=sender_gender, sender_id=sender.pk, receiver_gender=receiver_gender
            ).values_list('receiver_id', flat=True))

            sender_dob = sender.date_of_birth
            if sender_gender == 'M' and sender_dob:
                qs_age = receiver_model.objects.filter(date_of_birth__gt=sender_dob)
            elif sender_gender == 'F' and sender_dob:
                qs_age = receiver_model.objects.filter(date_of_birth__lt=sender_dob)
            else:
                qs_age = receiver_model.objects.all()

            try:
                exp = CandidateExpectation.objects.prefetch_related(
                    'nachathirams__nachathiram', 'sub_castes__sub_caste',
                    'districts__district', 'professions__profession', 'complexions__complexion',
                ).get(candidate_gender=sender_gender, candidate_id=sender.pk)
                matches = self._find_matches(exp, receiver_model, sent_ids, sender_gender, qs_age)
            except CandidateExpectation.DoesNotExist:
                matches = list(
                    qs_age.exclude(pk__in=sent_ids).exclude(whatsapp_number='').order_by('?')[:remaining]
                )

            if not matches:
                continue

            matches = matches[:remaining]

            if not dry_run:
                for receiver in matches:
                    token = BioToken.create_for_candidate(receiver_gender, receiver.pk)
                    BioSendLog.objects.create(
                        sender_gender=sender_gender, sender_id=sender.pk,
                        receiver_gender=receiver_gender, receiver_id=receiver.pk,
                        bio_token=token, month_year=week_key, status='pending',
                    )
                    prepared += 1
            else:
                self.stdout.write(f"  [DRY] {sender_gender}{sender.pk} ({sender.name}) → {len(matches)} பொருத்தங்கள்")
                prepared += len(matches)

        return prepared

    def _find_matches(self, exp, receiver_model, sent_ids, sender_gender, qs_age=None):
        qs = (qs_age if qs_age is not None else receiver_model.objects).exclude(pk__in=sent_ids)
        if exp.salary_min:
            qs = qs.filter(monthly_salary__gte=exp.salary_min)
        if exp.sevadosham_ok:
            qs = qs.filter(sevadosham=exp.sevadosham_ok)
        if exp.marital_status_ok:
            qs = qs.filter(status=exp.marital_status_ok)
        nach_ids = list(exp.nachathirams.values_list('nachathiram_id', flat=True))
        if nach_ids:
            qs = qs.filter(nachathiram_id__in=nach_ids)
        sc_ids = list(exp.sub_castes.values_list('sub_caste_id', flat=True))
        if sc_ids:
            qs = qs.filter(sub_caste_id__in=sc_ids)
        dist_ids = list(exp.districts.values_list('district_id', flat=True))
        if dist_ids:
            qs = qs.filter(district_id__in=dist_ids)
        prof_ids = list(exp.professions.values_list('profession_id', flat=True))
        if prof_ids:
            qs = qs.filter(profession_id__in=prof_ids)
        comp_ids = list(exp.complexions.values_list('complexion_id', flat=True))
        if comp_ids:
            qs = qs.filter(complexion_id__in=comp_ids)
        return list(qs.order_by('?')[:50])
