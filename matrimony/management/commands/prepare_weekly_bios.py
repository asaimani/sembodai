"""
Management command: prepare_weekly_bios
Processes all active candidates in batches — no HTTP timeout risk.

Usage:
  python manage.py prepare_weekly_bios
  python manage.py prepare_weekly_bios --dry-run
  python manage.py prepare_weekly_bios --batch-size 200

Railway Cron (every Sunday 6 AM IST = 12:30 AM UTC):
  30 0 * * 0   cd /app && python manage.py prepare_weekly_bios
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from collections import defaultdict
import time


class Command(BaseCommand):
    help = 'Prepare weekly bio matches (batched, no timeout risk)'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run',    action='store_true')
        parser.add_argument('--user-id',    type=int, default=None)
        parser.add_argument('--batch-size', type=int, default=500)

    def handle(self, *args, **options):
        from matrimony.models import (
            MaleCandidate, FemaleCandidate, BioSendLog,
            WeeklyBioRun, WeeklyBioConfig, MarriedCandidate,
        )
        from django.db.models import Q

        dry_run    = options['dry_run']
        user_id    = options.get('user_id')
        batch_size = options['batch_size']

        today = date.today()
        days_since_sunday = (today.weekday() + 1) % 7
        week_start = today - timedelta(days=days_since_sunday)
        week_end   = week_start + timedelta(days=6)
        week_key   = str(week_start)
        week_label = f"{week_start} முதல் {week_end} வரை"

        cfg = WeeklyBioConfig.get()

        # Block if already run
        if not dry_run and WeeklyBioRun.objects.filter(week_start=week_start).exists():
            self.stdout.write(self.style.ERROR(
                f"இந்த வாரம் ({week_label}) ஏற்கனவே இயக்கப்பட்டது."
            ))
            return

        self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}வார பயோ — {week_label}")

        # Cleanup
        if not dry_run:
            cutoff = (today - timedelta(days=cfg.bio_log_retention_days)).strftime('%Y-%m-%d')
            deleted, _ = BioSendLog.objects.filter(month_year__lt=cutoff).delete()
            if deleted:
                self.stdout.write(f"  {deleted} பழைய பதிவுகள் நீக்கப்பட்டன.")

            married_cutoff = timezone.now() - timedelta(days=cfg.married_cleanup_days)
            old_married = list(MarriedCandidate.objects.filter(married_at__lt=married_cutoff))
            for mc in old_married:
                BioSendLog.objects.filter(sender_gender=mc.gender, sender_id=mc.candidate_id).delete()
                BioSendLog.objects.filter(receiver_gender=mc.gender, receiver_id=mc.candidate_id).delete()
                if mc.gender == 'M':
                    MaleCandidate.objects.filter(pk=mc.candidate_id).delete()
                else:
                    FemaleCandidate.objects.filter(pk=mc.candidate_id).delete()
            if old_married:
                MarriedCandidate.objects.filter(married_at__lt=married_cutoff).delete()
                self.stdout.write(f"  {len(old_married)} திருமணமான வரன்கள் நீக்கப்பட்டன.")

        t0 = time.time()

        self.stdout.write("\nஆண் → பெண்:")
        mp, mn_m, nw_m = self._prepare(MaleCandidate, FemaleCandidate, 'M', 'F', week_key, cfg, batch_size, dry_run)

        self.stdout.write("\nபெண் → ஆண்:")
        fp, mn_f, nw_f = self._prepare(FemaleCandidate, MaleCandidate, 'F', 'M', week_key, cfg, batch_size, dry_run)

        total   = mp + fp
        elapsed = int(time.time() - t0)

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
                matches_created=total,
                notes=(
                    f"வார இயக்கம் {week_label}. மொத்தம் {total} பொருத்தங்கள். "
                    f"ஆண்: {mp} matched, {mn_m} no-match, {nw_m} no-WA. "
                    f"பெண்: {fp} matched, {mn_f} no-match, {nw_f} no-WA. "
                    f"நேரம்: {elapsed}s."
                ),
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nமொத்தம் {total} பொருத்தங்கள். நேரம்: {elapsed}s"
        ))

    def _get_limit(self, candidate, cfg):
        is_rem = (candidate.status and candidate.status.code == 'remarriage')
        if is_rem:
            code = candidate.premium_type.code if candidate.premium_type else 'silver'
            lmap = {
                'silver': cfg.remarriage_silver_limit,
                'gold':   cfg.remarriage_gold_limit,
                'platinum': cfg.remarriage_platinum_limit,
                'diamond':  cfg.remarriage_diamond_limit,
            }
            limit = lmap.get(code, cfg.remarriage_silver_limit)
        elif candidate.premium_type:
            limit = candidate.premium_type.weekly_limit
        else:
            limit = cfg.default_weekly_limit
        return None if limit == 0 else limit

    def _prepare(self, sender_model, receiver_model, sg, rg, week_key, cfg, batch_size, dry_run):
        from matrimony.models import CandidateExpectation, BioToken, BioSendLog
        from django.db.models import Q, Count

        today = date.today()
        prepared = no_match = no_wa = 0

        base_qs = sender_model.objects.select_related(
            'premium_type', 'status'
        ).filter(
            Q(premium_end_date__isnull=True) | Q(premium_end_date__gte=today)
        ).exclude(status__code='married').order_by('pk')

        total = base_qs.count()
        self.stdout.write(f"  வரன்கள்: {total:,} | batch: {batch_size}")

        # Pre-fetch this week's counts for ALL senders in ONE query
        week_counts = dict(
            BioSendLog.objects.filter(sender_gender=sg, month_year=week_key)
            .values('sender_id').annotate(n=Count('id')).values_list('sender_id', 'n')
        )

        offset = 0
        batch_num = 0
        while True:
            batch = list(base_qs[offset: offset + batch_size])
            if not batch:
                break

            batch_num += 1
            batch_ids = [s.pk for s in batch]
            self.stdout.write(f"  Batch {batch_num}: {offset+1}–{offset+len(batch)} / {total}")

            # Bulk-fetch all-time sent pairs for this batch (ONE query per batch)
            sent_map = defaultdict(set)
            for sid, rid in BioSendLog.objects.filter(
                sender_gender=sg, sender_id__in=batch_ids, receiver_gender=rg
            ).values_list('sender_id', 'receiver_id'):
                sent_map[sid].add(rid)

            for sender in batch:
                if not sender.whatsapp_number:
                    no_wa += 1
                    continue

                limit = self._get_limit(sender, cfg)
                already = week_counts.get(sender.pk, 0)

                if limit is not None and already > limit:
                    if not dry_run:
                        excess = list(
                            BioSendLog.objects.filter(
                                sender_gender=sg, sender_id=sender.pk,
                                month_year=week_key, status='pending'
                            ).order_by('-prepared_at').values_list('pk', flat=True)[:already - limit]
                        )
                        if excess:
                            BioSendLog.objects.filter(pk__in=excess).delete()
                    already = limit

                if limit is not None and already >= limit:
                    continue

                remaining = (limit - already) if limit is not None else 999
                sent_ids  = sent_map[sender.pk]
                sender_dob = sender.date_of_birth
                is_divorced = (sender.status and sender.status.code == 'remarriage')

                if cfg.match_divorced_only:
                    rqs = receiver_model.objects.filter(status__code='remarriage') if is_divorced \
                          else receiver_model.objects.exclude(status__code='remarriage')
                else:
                    rqs = receiver_model.objects.all()

                if cfg.match_age_strict and sender_dob:
                    qs_age = rqs.filter(date_of_birth__gt=sender_dob) if sg == 'M' \
                             else rqs.filter(date_of_birth__lt=sender_dob)
                else:
                    qs_age = rqs.all()

                try:
                    exp = CandidateExpectation.objects.prefetch_related(
                        'nachathirams__nachathiram', 'sub_castes__sub_caste',
                        'districts__district', 'professions__profession',
                        'complexions__complexion',
                    ).get(candidate_gender=sg, candidate_id=sender.pk)
                    matches = self._find_matches(exp, receiver_model, sent_ids, qs_age, cfg.max_receivers_per_run)
                except CandidateExpectation.DoesNotExist:
                    matches = list(
                        qs_age.exclude(pk__in=sent_ids).exclude(whatsapp_number='')
                        .order_by('-premium_start_date')[:remaining]
                    )

                if not matches:
                    no_match += 1
                    continue

                matches = matches[:remaining]

                if not dry_run:
                    for receiver in matches:
                        token = BioToken.create_for_candidate(rg, receiver.pk)
                        BioSendLog.objects.create(
                            sender_gender=sg, sender_id=sender.pk,
                            receiver_gender=rg, receiver_id=receiver.pk,
                            bio_token=token, month_year=week_key, status='pending',
                        )
                    week_counts[sender.pk] = already + len(matches)
                    prepared += len(matches)
                else:
                    self.stdout.write(f"    [DRY] {sg}{sender.pk} → {len(matches)}")
                    prepared += len(matches)

            offset += batch_size

        return prepared, no_match, no_wa

    def _find_matches(self, exp, receiver_model, sent_ids, qs_age, max_receivers):
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
        return list(qs.order_by('-premium_start_date')[:max_receivers])
