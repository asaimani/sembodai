from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
import random


class Command(BaseCommand):
    help = 'Prepare weekly bio matches for all candidates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be prepared without saving',
        )

    def handle(self, *args, **options):
        from matrimony.models import (
            MaleCandidate, FemaleCandidate,
            CandidateExpectation, BioToken, BioSendLog,
            PremiumType,
        )
        dry_run = options['dry_run']
        month_year = date.today().strftime('%Y-%m')
        total_prepared = 0

        self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}வார பயோ தயாரிப்பு தொடங்கியது — {month_year}")

        # Process male candidates → find female matches
        total_prepared += self._prepare_for_gender(
            sender_model=MaleCandidate,
            receiver_model=FemaleCandidate,
            sender_gender='M',
            receiver_gender='F',
            month_year=month_year,
            dry_run=dry_run,
        )

        # Process female candidates → find male matches
        total_prepared += self._prepare_for_gender(
            sender_model=FemaleCandidate,
            receiver_model=MaleCandidate,
            sender_gender='F',
            receiver_gender='M',
            month_year=month_year,
            dry_run=dry_run,
        )

        self.stdout.write(self.style.SUCCESS(
            f"{'[DRY RUN] ' if dry_run else ''}மொத்தம் {total_prepared} பொருத்தங்கள் தயார்."
        ))

    def _get_monthly_limit(self, candidate):
        if candidate.premium_type:
            limit = candidate.premium_type.monthly_limit
            return None if limit == 0 else limit  # 0 = unlimited
        return 5  # default Silver limit

    def _prepare_for_gender(self, sender_model, receiver_model,
                             sender_gender, receiver_gender, month_year, dry_run):
        from matrimony.models import CandidateExpectation, BioToken, BioSendLog
        prepared = 0

        senders = sender_model.objects.select_related('premium_type').all()

        for sender in senders:
            # Skip if no WhatsApp number
            if not sender.whatsapp_number:
                continue

            limit = self._get_monthly_limit(sender)

            # Enforce limit — delete excess pending records if limit was reduced
            if limit is not None:
                all_this_month = BioSendLog.objects.filter(
                    sender_gender=sender_gender,
                    sender_id=sender.pk,
                    month_year=month_year,
                ).order_by('prepared_at')
                total_this_month = all_this_month.count()
                if total_this_month > limit:
                    # Delete excess pending ones (keep sent ones)
                    excess = total_this_month - limit
                    excess_ids = list(
                        all_this_month.filter(status='pending')
                        .order_by('-prepared_at')
                        .values_list('pk', flat=True)[:excess]
                    )
                    BioSendLog.objects.filter(pk__in=excess_ids).delete()

            # Count already prepared this month
            already_prepared = BioSendLog.objects.filter(
                sender_gender=sender_gender,
                sender_id=sender.pk,
                month_year=month_year,
            ).count()

            if limit is not None and already_prepared >= limit:
                continue  # quota full

            remaining = (limit - already_prepared) if limit is not None else 999

            # Get already sent receiver IDs (all time — no repeats ever)
            sent_ids = set(BioSendLog.objects.filter(
                sender_gender=sender_gender,
                sender_id=sender.pk,
                receiver_gender=receiver_gender,
            ).values_list('receiver_id', flat=True))

            # Default age logic: male must be older than female
            sender_dob = sender.date_of_birth
            if sender_gender == 'M' and sender_dob:
                qs_age = receiver_model.objects.filter(date_of_birth__gt=sender_dob)
            elif sender_gender == 'F' and sender_dob:
                qs_age = receiver_model.objects.filter(date_of_birth__lt=sender_dob)
            else:
                qs_age = receiver_model.objects.all()

            # Get expectation if exists
            try:
                exp = CandidateExpectation.objects.prefetch_related(
                    'nachathirams__nachathiram',
                    'sub_castes__sub_caste',
                    'districts__district',
                    'professions__profession',
                    'complexions__complexion',
                ).get(candidate_gender=sender_gender, candidate_id=sender.pk)
                matches = self._find_matches(exp, receiver_model, sent_ids, sender_gender, qs_age)
            except CandidateExpectation.DoesNotExist:
                # No expectations — random matches
                matches = list(
                    qs_age.exclude(pk__in=sent_ids)
                    .exclude(whatsapp_number='')
                    .order_by('?')[:remaining]
                )

            if not matches:
                continue

            matches = matches[:remaining]

            if not dry_run:
                for receiver in matches:
                    token = BioToken.create_for_candidate(receiver_gender, receiver.pk)
                    BioSendLog.objects.create(
                        sender_gender=sender_gender,
                        sender_id=sender.pk,
                        receiver_gender=receiver_gender,
                        receiver_id=receiver.pk,
                        bio_token=token,
                        month_year=month_year,
                        status='pending',
                    )
                    prepared += 1
            else:
                self.stdout.write(
                    f"  [DRY] {sender_gender}{sender.pk} ({sender.name}) → "
                    f"{len(matches)} பொருத்தங்கள்"
                )
                prepared += len(matches)

        return prepared

    def _find_matches(self, exp, receiver_model, sent_ids, sender_gender, qs_age=None):
        qs = (qs_age if qs_age is not None else receiver_model.objects).exclude(pk__in=sent_ids)

        if exp.salary_min:
            qs = qs.filter(monthly_salary__gte=exp.salary_min)

        # Sevadosham filter
        if exp.sevadosham_ok:
            qs = qs.filter(sevadosham=exp.sevadosham_ok)

        # Marital status filter
        if exp.marital_status_ok:
            qs = qs.filter(status=exp.marital_status_ok)

        # Nachathiram filter
        nach_ids = list(exp.nachathirams.values_list('nachathiram_id', flat=True))
        if nach_ids:
            qs = qs.filter(nachathiram_id__in=nach_ids)

        # Sub caste filter
        sc_ids = list(exp.sub_castes.values_list('sub_caste_id', flat=True))
        if sc_ids:
            qs = qs.filter(sub_caste_id__in=sc_ids)

        # District filter
        dist_ids = list(exp.districts.values_list('district_id', flat=True))
        if dist_ids:
            qs = qs.filter(district_id__in=dist_ids)

        # Profession filter
        prof_ids = list(exp.professions.values_list('profession_id', flat=True))
        if prof_ids:
            qs = qs.filter(profession_id__in=prof_ids)

        # Complexion filter
        comp_ids = list(exp.complexions.values_list('complexion_id', flat=True))
        if comp_ids:
            qs = qs.filter(complexion_id__in=comp_ids)

        return list(qs.order_by('?')[:50])  # random order, take up to 50 then slice by quota
