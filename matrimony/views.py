from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import date, timedelta
from .models import *
from .forms import *


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'தவறான பயனர்பெயர் அல்லது கடவுச்சொல்')
    return render(request, 'matrimony/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    today = date.today()
    male_count = MaleCandidate.objects.count()
    female_count = FemaleCandidate.objects.count()
    total = male_count + female_count
    new_male = MaleCandidate.objects.filter(created_at__date=today).order_by('-created_at')[:20]
    new_female = FemaleCandidate.objects.filter(created_at__date=today).order_by('-created_at')[:20]
    expired_male_qs = MaleCandidate.objects.filter(premium_end_date__lt=today)
    expired_female_qs = FemaleCandidate.objects.filter(premium_end_date__lt=today)
    expired_male_count = expired_male_qs.count()
    expired_female_count = expired_female_qs.count()
    expired_entries = list(expired_male_qs.order_by('-premium_end_date')[:20]) + list(expired_female_qs.order_by('-premium_end_date')[:20])
    context = {
        'male_count': male_count,
        'female_count': female_count,
        'total': total,
        'new_entries': list(new_male) + list(new_female),
        'expired_entries': expired_entries,
        'expired_count': expired_male_count + expired_female_count,
        'expired_male_count': expired_male_count,
        'expired_female_count': expired_female_count,
        'today': today,
    }
    return render(request, 'matrimony/dashboard.html', context)


@login_required
def candidate_list(request):
    gender = request.GET.get('gender', '')
    search = request.GET.get('search', '')
    age_min = request.GET.get('age_min', '')
    age_max = request.GET.get('age_max', '')
    rasi_id = request.GET.get('rasi', '')
    nachathiram_id = request.GET.get('nachathiram', '')
    salary_min = request.GET.get('salary_min', '')
    status_filter = request.GET.get('status', '')
    district_id = request.GET.get('district', '')
    created_by_id = request.GET.get('created_by', '')
    page_num = request.GET.get('page', 1)
    PER_PAGE = 50

    def apply_filters(qs):
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(uid__icontains=search) | Q(old_reg_no__icontains=search))
        if rasi_id:
            qs = qs.filter(rasi_id=rasi_id)
        if nachathiram_id:
            qs = qs.filter(nachathiram_id=nachathiram_id)
        if salary_min:
            try:
                qs = qs.filter(monthly_salary__gte=int(salary_min))
            except ValueError:
                pass
        if status_filter:
            qs = qs.filter(status__code=status_filter)
        if district_id:
            qs = qs.filter(district_id=district_id)
        if created_by_id:
            qs = qs.filter(created_by_id=created_by_id)
        if age_min:
            try:
                max_dob = date(date.today().year - int(age_min), date.today().month, date.today().day)
                qs = qs.filter(date_of_birth__lte=max_dob)
            except ValueError:
                pass
        if age_max:
            try:
                min_dob = date(date.today().year - int(age_max), date.today().month, date.today().day)
                qs = qs.filter(date_of_birth__gte=min_dob)
            except ValueError:
                pass
        return qs

    base_select = {'select_related': ['rasi', 'nachathiram', 'profession', 'state', 'district', 'created_by']}
    MAX_RESULTS = 500

    if gender == 'M':
        qs = apply_filters(
            MaleCandidate.objects.all()
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        total_count = min(qs.count(), MAX_RESULTS)
        paginator = Paginator(qs[:MAX_RESULTS], PER_PAGE)
        page_obj = paginator.get_page(page_num)
        candidates = [('M', c) for c in page_obj]

    elif gender == 'F':
        qs = apply_filters(
            FemaleCandidate.objects.all()
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        total_count = min(qs.count(), MAX_RESULTS)
        paginator = Paginator(qs[:MAX_RESULTS], PER_PAGE)
        page_obj = paginator.get_page(page_num)
        candidates = [('F', c) for c in page_obj]

    else:
        # Both genders: paginate males and females separately, interleave by created_at
        # To avoid in-memory sort of 2M rows, paginate each independently
        # and show them as two separate sorted querysets using DB ordering
        males_qs_full = apply_filters(
            MaleCandidate.objects.all()
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        females_qs_full = apply_filters(
            FemaleCandidate.objects.all()
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        # Count before slicing to get real totals, capped at MAX_RESULTS
        male_count = min(males_qs_full.count(), MAX_RESULTS)
        female_count = min(females_qs_full.count(), MAX_RESULTS)
        total_count = male_count + female_count
        # Slice after counting
        males_qs = males_qs_full[:MAX_RESULTS]
        females_qs = females_qs_full[:MAX_RESULTS]

        # Alternate pages: odd pages lean male, even pages lean female
        # Simple approach: show PER_PAGE/2 from each per page
        half = PER_PAGE // 2
        try:
            page_num_int = int(page_num)
        except (ValueError, TypeError):
            page_num_int = 1
        offset = (page_num_int - 1) * half

        males_page = list(males_qs[offset:offset + half])
        females_page = list(females_qs[offset:offset + half])

        # Interleave
        candidates = []
        for i in range(max(len(males_page), len(females_page))):
            if i < len(males_page):
                candidates.append(('M', males_page[i]))
            if i < len(females_page):
                candidates.append(('F', females_page[i]))

        import math
        total_pages = math.ceil(max(male_count, female_count) / half) if total_count else 1
        page_obj = type('PageObj', (), {
            'number': page_num_int,
            'has_previous': page_num_int > 1,
            'has_next': page_num_int < total_pages,
            'previous_page_number': lambda self: self.number - 1,
            'next_page_number': lambda self: self.number + 1,
            'paginator': type('Pag', (), {'num_pages': total_pages, 'count': total_count})(),
        })()

    rasis = Rasi.objects.all()
    nachathirams = Nachathiram.objects.all()

    # Build district and user dropdowns from FULL candidate DB (not filtered/paginated)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    _m_dist  = MaleCandidate.objects.exclude(district=None).values_list('district_id', flat=True).distinct()
    _f_dist  = FemaleCandidate.objects.exclude(district=None).values_list('district_id', flat=True).distinct()
    _m_users = MaleCandidate.objects.exclude(created_by=None).values_list('created_by_id', flat=True).distinct()
    _f_users = FemaleCandidate.objects.exclude(created_by=None).values_list('created_by_id', flat=True).distinct()
    all_dist_ids = set(list(_m_dist) + list(_f_dist))
    all_user_ids = set(list(_m_users) + list(_f_users))
    districts        = District.objects.filter(pk__in=all_dist_ids).order_by('name')
    created_by_users = User.objects.filter(pk__in=all_user_ids).order_by('username')

    context = {
        'candidates': candidates,
        'page_obj': page_obj,
        'total_count': total_count,
        'rasis': rasis,
        'nachathirams': nachathirams,
        'districts': districts,
        'created_by_users': created_by_users,
        'gender': gender,
        'search': search,
    }
    return render(request, 'matrimony/candidate_list.html', context)


def _save_jathagam(candidate, post_data):
    """
    Reads multi-select planet values from POST and saves to JathagamEntry.
    Only runs when the popup JS wrote sentinel field 'jathagam_submitted'.
    This prevents accidental deletion when saving without touching jathagam.
    """
    from .models import JathagamEntry, Planet

    if not post_data.get('jathagam_submitted'):
        return

    gender = 'M' if isinstance(candidate, MaleCandidate) else 'F'

    # Delete all existing entries for this candidate
    JathagamEntry.objects.filter(
        candidate_gender=gender,
        candidate_id=candidate.pk,
    ).delete()

    chart_map = {'rasi': 'R', 'navamsam': 'N'}

    # Collect all planet PKs from POST first
    all_pids = set()
    for prefix in chart_map:
        for house in range(1, 13):
            for pid in post_data.getlist(f'{prefix}_h{house}[]'):
                try:
                    all_pids.add(int(pid))
                except ValueError:
                    pass

    # Single DB query for all planets needed — no N+1
    planet_map = Planet.objects.in_bulk(list(all_pids))

    entries = []
    for prefix, chart_type in chart_map.items():
        for house in range(1, 13):
            planet_ids = post_data.getlist(f'{prefix}_h{house}[]')
            for order, pid in enumerate(planet_ids, start=1):
                try:
                    planet = planet_map.get(int(pid))
                    if planet:
                        entries.append(JathagamEntry(
                            candidate_gender=gender,
                            candidate_id=candidate.pk,
                            chart_type=chart_type,
                            house_number=house,
                            planet=planet,
                            order=order,
                        ))
                except ValueError:
                    continue
    if entries:
        JathagamEntry.objects.bulk_create(entries)


MAX_PHOTO_SIZE_MB = 5  # Maximum upload size in MB

def _save_photos(candidate, files, is_male):
    if not files:
        return
    photo = files[0]
    # Validate file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if photo.content_type not in allowed_types:
        raise ValueError("புகைப்படம் JPEG, PNG அல்லது WebP வடிவத்தில் இருக்க வேண்டும்.")
    # Validate file size
    max_bytes = MAX_PHOTO_SIZE_MB * 1024 * 1024
    if photo.size > max_bytes:
        raise ValueError(f"புகைப்படம் அளவு {MAX_PHOTO_SIZE_MB}MB-ஐ தாண்டக்கூடாது. தற்போதைய அளவு: {photo.size // (1024*1024)}MB")
    # Only 1 photo allowed - delete existing first
    for existing in candidate.photos.all():
        import os
        if existing.photo and os.path.isfile(existing.photo.path):
            os.remove(existing.photo.path)
        existing.delete()
    # Save only first photo, renamed to UID
    if is_male:
        CandidatePhoto.objects.create(male_candidate=candidate, photo=photo, is_primary=True)
    else:
        CandidatePhoto.objects.create(female_candidate=candidate, photo=photo, is_primary=True)


def _save_family_members(candidate, post_data):
    gender = 'M' if isinstance(candidate, MaleCandidate) else 'F'
    # Delete existing and re-save
    FamilyMember.objects.filter(candidate_gender=gender, candidate_id=candidate.pk).delete()
    for i in range(1, 6):
        name = post_data.get(f'family_name_{i}', '').strip()
        if not name:
            continue
        relation_id = post_data.get(f'family_relation_{i}', '') or None
        marital_id  = post_data.get(f'family_marital_{i}', '') or None
        FamilyMember.objects.create(
            candidate_gender = gender,
            candidate_id     = candidate.pk,
            name             = name,
            education        = post_data.get(f'family_education_{i}', '').strip(),
            relation_id      = relation_id,
            marital_status_id= marital_id,
            job_info         = post_data.get(f'family_job_{i}', '').strip(),
            order            = i,
        )


def _save_expectation(candidate, gender, post_data):
    """Save expectation fields from the main candidate form POST."""
    from .models import (CandidateExpectation, ExpectationNachathiram,
                          ExpectationSubCaste, ExpectationDistrict,
                          ExpectationProfession, ExpectationComplexion,
                          Sevadosham, OwnHouse, MaritalStatus,
                          Nachathiram, SubCaste, District, Profession, Complexion)

    exp, _ = CandidateExpectation.objects.get_or_create(
        candidate_gender=gender, candidate_id=candidate.pk)

    exp.salary_min    = post_data.get('exp_salary_min') or None
    exp.education_min = post_data.get('exp_education_min', '').strip()
    exp.job_type      = post_data.get('exp_job_type', 'any')
    exp.notes         = post_data.get('exp_notes', '').strip()

    sev  = post_data.get('exp_sevadosham_ok')
    own  = post_data.get('exp_own_house_pref')
    mar  = post_data.get('exp_marital_status_ok')

    exp.sevadosham_ok     = Sevadosham.objects.filter(pk=sev).first() if sev else None
    exp.own_house_pref    = OwnHouse.objects.filter(pk=own).first() if own else None
    exp.marital_status_ok = MaritalStatus.objects.filter(pk=mar).first() if mar else None
    exp.save()

    exp.nachathirams.all().delete()
    for nid in post_data.getlist('exp_nachathirams[]'):
        n = Nachathiram.objects.filter(pk=nid).first()
        if n: ExpectationNachathiram.objects.create(expectation=exp, nachathiram=n)

    exp.sub_castes.all().delete()
    for sid in post_data.getlist('exp_sub_castes[]'):
        s = SubCaste.objects.filter(pk=sid).first()
        if s: ExpectationSubCaste.objects.create(expectation=exp, sub_caste=s)

    exp.districts.all().delete()
    for did in post_data.getlist('exp_districts[]'):
        d = District.objects.filter(pk=did).first()
        if d: ExpectationDistrict.objects.create(expectation=exp, district=d)

    exp.professions.all().delete()
    for pid in post_data.getlist('exp_professions[]'):
        p = Profession.objects.filter(pk=pid).first()
        if p: ExpectationProfession.objects.create(expectation=exp, profession=p)

    exp.complexions.all().delete()
    for cid in post_data.getlist('exp_complexions[]'):
        c = Complexion.objects.filter(pk=cid).first()
        if c: ExpectationComplexion.objects.create(expectation=exp, complexion=c)


@login_required
def candidate_add(request):
    gender = request.GET.get('gender', 'M')
    is_male = gender == 'M'
    FormClass = MaleCandidateForm if is_male else FemaleCandidateForm

    if request.method == 'POST':
        gender = request.POST.get('_gender', gender)  # preserve gender on POST
        is_male = gender == 'M'
        FormClass = MaleCandidateForm if is_male else FemaleCandidateForm
        form = FormClass(request.POST)
        photos = request.FILES.getlist('photos')
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.created_by = request.user

            # Always force active status if form submitted with active or empty
            from .models import CandidateStatus
            status_id = request.POST.get('status', '')
            if status_id:
                try:
                    candidate.status = CandidateStatus.objects.get(pk=int(status_id))
                except Exception:
                    pass
            if not candidate.status_id:
                active_status = CandidateStatus.objects.filter(code='searching').first() or CandidateStatus.objects.filter(code='active').first()
                if active_status:
                    candidate.status = active_status
            candidate.save()
            _save_expectation(candidate, gender, request.POST)
            _save_jathagam(candidate, request.POST)
            _save_family_members(candidate, request.POST)
            try:
                _save_photos(candidate, photos, is_male)
            except ValueError as e:
                messages.error(request, str(e))
            messages.success(request, f'விண்ணப்பம் வெற்றிகரமாக சேர்க்கப்பட்டது. UID: {candidate.uid}')
            return redirect('candidate_detail', gender=gender, pk=candidate.pk)
    else:
        form = FormClass()

    from .models import (Planet, Relation, MaritalStatus, Height, Sevadosham,
                           OwnHouse, Nachathiram, SubCaste, District, Profession, Complexion)
    empty_map = {'R': {h: '' for h in range(1, 13)}, 'N': {h: '' for h in range(1, 13)}}
    return render(request, 'matrimony/candidate_form.html', {
        'form': form, 'gender': gender,
        'title': 'புதிய விண்ணப்பம்',
        'planets': Planet.objects.all(),
        'relations': Relation.objects.all(),
        'marital_statuses': MaritalStatus.objects.all(),
        'family_members': [],
        'jathagam_map': empty_map,
        'expectation': None,
        'exp_nachathiram_ids': [],
        'exp_sub_caste_ids': [],
        'exp_district_ids': [],
        'exp_profession_ids': [],
        'exp_complexion_ids': [],
        'heights': Height.objects.all(),
        'sevadoshams': Sevadosham.objects.all(),
        'own_houses': OwnHouse.objects.all(),
        'nachathirams': Nachathiram.objects.all(),
        'all_sub_castes': SubCaste.objects.all(),
        'all_districts': District.objects.all(),
        'professions': Profession.objects.all(),
        'complexions': Complexion.objects.all(),
    })


def _get_candidate(gender, pk):
    if gender == 'M':
        return get_object_or_404(MaleCandidate, pk=pk)
    return get_object_or_404(FemaleCandidate, pk=pk)


@login_required
def candidate_detail(request, gender, pk):
    candidate = _get_candidate(gender, pk)
    gender_code = 'M' if gender == 'M' else 'F'
    family_members = FamilyMember.objects.filter(candidate_gender=gender_code, candidate_id=candidate.pk)
    jathagam_map = candidate.get_jathagam_map()
    return render(request, 'matrimony/candidate_detail.html', {
        'candidate': candidate,
        'gender': gender,
        'family_members': family_members,
        'jathagam_map': jathagam_map,
    })


@login_required
def candidate_edit(request, gender, pk):
    candidate = _get_candidate(gender, pk)
    is_male = gender == 'M'
    FormClass = MaleCandidateForm if is_male else FemaleCandidateForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=candidate)
        if form.is_valid():
            saved = form.save(commit=False)
            # Explicitly save status from POST
            from .models import CandidateStatus
            status_id = request.POST.get('status', '')
            if status_id:
                try:
                    saved.status = CandidateStatus.objects.get(pk=int(status_id))
                except Exception:
                    pass
            elif not saved.status_id:
                active = CandidateStatus.objects.filter(code='searching').first() or CandidateStatus.objects.filter(code='active').first()
                if active:
                    saved.status = active
            saved.save()
            form.save_m2m()
            _save_expectation(saved, gender, request.POST)
            photos = request.FILES.getlist('photos')
            try:
                _save_photos(candidate, photos, is_male)
            except ValueError as e:
                messages.error(request, str(e))
            _save_jathagam(saved, request.POST)
            _save_family_members(saved, request.POST)
            messages.success(request, 'விண்ணப்பம் புதுப்பிக்கப்பட்டது.')
            return redirect('candidate_detail', gender=gender, pk=candidate.pk)
    else:
        form = FormClass(instance=candidate)

    from .models import (Planet, Relation, MaritalStatus, CandidateExpectation,
                           Height, Sevadosham, OwnHouse, Nachathiram, SubCaste,
                           District, Profession, Complexion)
    gender_code = 'M' if is_male else 'F'
    family_members = list(FamilyMember.objects.filter(candidate_gender=gender_code, candidate_id=candidate.pk))
    jathagam_map = candidate.get_jathagam_map()
    expectation = None
    exp_nachathiram_ids = exp_sub_caste_ids = exp_district_ids = []
    exp_profession_ids  = exp_complexion_ids = []
    try:
        expectation = CandidateExpectation.objects.get(candidate_gender=gender, candidate_id=candidate.pk)
        exp_nachathiram_ids = list(expectation.nachathirams.values_list('nachathiram_id', flat=True))
        exp_sub_caste_ids   = list(expectation.sub_castes.values_list('sub_caste_id', flat=True))
        exp_district_ids    = list(expectation.districts.values_list('district_id', flat=True))
        exp_profession_ids  = list(expectation.professions.values_list('profession_id', flat=True))
        exp_complexion_ids  = list(expectation.complexions.values_list('complexion_id', flat=True))
    except CandidateExpectation.DoesNotExist:
        pass
    return render(request, 'matrimony/candidate_form.html', {
        'form': form, 'candidate': candidate, 'gender': gender,
        'title': 'திருத்து',
        'planets': Planet.objects.all(),
        'relations': Relation.objects.all(),
        'marital_statuses': MaritalStatus.objects.all(),
        'family_members': family_members,
        'jathagam_map': jathagam_map,
        'expectation': expectation,
        'exp_nachathiram_ids': exp_nachathiram_ids,
        'exp_sub_caste_ids': exp_sub_caste_ids,
        'exp_district_ids': exp_district_ids,
        'exp_profession_ids': exp_profession_ids,
        'exp_complexion_ids': exp_complexion_ids,
        'heights': Height.objects.all(),
        'sevadoshams': Sevadosham.objects.all(),
        'own_houses': OwnHouse.objects.all(),
        'nachathirams': Nachathiram.objects.all(),
        'all_sub_castes': SubCaste.objects.all(),
        'all_districts': District.objects.all(),
        'professions': Profession.objects.all(),
        'complexions': Complexion.objects.all(),
    })


@login_required
def candidate_print(request, gender, pk):
    import base64, os
    candidate = _get_candidate(gender, pk)
    admin_profile = None
    try:
        admin_profile = request.user.adminprofile
    except Exception:
        pass

    photo_base64 = None
    first_photo = candidate.photos.first()
    if first_photo:
        try:
            photo_path = first_photo.photo.path
            if os.path.exists(photo_path):
                with open(photo_path, 'rb') as img_file:
                    ext = os.path.splitext(photo_path)[1].lower().replace('.', '')
                    if ext == 'jpg': ext = 'jpeg'
                    photo_base64 = f"data:image/{ext};base64,{base64.b64encode(img_file.read()).decode()}"
        except Exception:
            photo_base64 = None

    gender_code = 'M' if gender == 'M' else 'F'
    family_members = FamilyMember.objects.filter(candidate_gender=gender_code, candidate_id=candidate.pk)
    jathagam_map = candidate.get_jathagam_map()
    is_plain = request.GET.get('plain') == '1'
    template = 'matrimony/candidate_print_plain.html' if is_plain else 'matrimony/candidate_print.html'
    return render(request, template, {
        'candidate': candidate,
        'admin_profile': admin_profile,
        'photo_base64': photo_base64,
        'gender': gender,
        'family_members': family_members,
        'jathagam_map': jathagam_map,
    })






@login_required
def candidate_delete(request, gender, pk):
    if not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("அனுமதி இல்லை")
    if gender == 'M':
        candidate = get_object_or_404(MaleCandidate, pk=pk)
    else:
        candidate = get_object_or_404(FemaleCandidate, pk=pk)
    if request.method == 'POST':
        import os
        # Delete family members
        FamilyMember.objects.filter(candidate_gender=gender, candidate_id=pk).delete()
        # Delete jathagam entries
        from .models import JathagamEntry
        JathagamEntry.objects.filter(candidate_gender=gender, candidate_id=pk).delete()
        # Delete photo files from disk
        for photo in candidate.photos.all():
            if photo.photo and os.path.isfile(photo.photo.path):
                os.remove(photo.photo.path)
        candidate.delete()
        return redirect('candidate_list')
    return render(request, 'matrimony/candidate_confirm_delete.html', {
        'candidate': candidate, 'gender': gender
    })

@login_required
def delete_photo(request, photo_id):
    # Accept both GET and POST
    photo = get_object_or_404(CandidatePhoto, pk=photo_id)
    candidate = photo.candidate
    candidate_pk = candidate.pk
    gender = 'M' if isinstance(candidate, MaleCandidate) else 'F'
    import os
    try:
        path = photo.photo.path
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
    photo.delete()
    messages.success(request, 'புகைப்படம் நீக்கப்பட்டது.')
    return redirect('candidate_edit', gender=gender, pk=candidate_pk)


@login_required
def get_districts(request):
    state_id = request.GET.get('state_id')
    districts = District.objects.filter(state_id=state_id).values('id', 'name').order_by('order', 'name')
    return JsonResponse(list(districts), safe=False)


@login_required
def get_sub_castes(request):
    caste_id = request.GET.get('caste_id')
    sub_castes = SubCaste.objects.filter(caste_id=caste_id).values('id', 'name')
    return JsonResponse(list(sub_castes), safe=False)


@login_required
def get_nachathirams(request):
    rasi_id = request.GET.get('rasi_id')
    nachathirams = Nachathiram.objects.filter(rasi_id=rasi_id).values('id', 'name')
    return JsonResponse(list(nachathirams), safe=False)



def _run_weekly_bios(user, week_start, week_end, week_key):
    """Run weekly bio matching directly from view."""
    from .models import (MaleCandidate, FemaleCandidate, CandidateExpectation,
                          BioToken, BioSendLog, WeeklyBioRun)
    from datetime import date, timedelta

    # Delete BioSendLog older than 6 months
    cutoff = (date.today() - timedelta(days=180)).strftime('%Y-%m-%d')
    BioSendLog.objects.filter(month_year__lt=cutoff).delete()

    def get_weekly_limit(candidate):
        if candidate.premium_type:
            limit = candidate.premium_type.weekly_limit
            return None if limit == 0 else limit
        return 5

    def prepare_gender(sender_model, receiver_model, sender_gender, receiver_gender):
        from datetime import date as _date
        today = _date.today()
        prepared = 0
        # Only active (non-expired) candidates as senders
        senders = sender_model.objects.select_related('premium_type').filter(
            Q(premium_end_date__isnull=True) | Q(premium_end_date__gte=today)
        )
        for sender in senders:
            if not sender.whatsapp_number:
                continue
            limit = get_weekly_limit(sender)
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
                from .models import CandidateExpectation
                exp = CandidateExpectation.objects.prefetch_related(
                    'nachathirams__nachathiram', 'sub_castes__sub_caste',
                    'districts__district', 'professions__profession', 'complexions__complexion',
                ).get(candidate_gender=sender_gender, candidate_id=sender.pk)
                matches = _find_matches_inline(exp, receiver_model, sent_ids, qs_age)
            except CandidateExpectation.DoesNotExist:
                matches = list(
                    qs_age.exclude(pk__in=sent_ids).exclude(whatsapp_number='').order_by('-created_at')[:remaining]
                )

            if not matches:
                continue
            matches = matches[:remaining]
            for receiver in matches:
                token = BioToken.create_for_candidate(receiver_gender, receiver.pk)
                BioSendLog.objects.create(
                    sender_gender=sender_gender, sender_id=sender.pk,
                    receiver_gender=receiver_gender, receiver_id=receiver.pk,
                    bio_token=token, month_year=week_key, status='pending',
                )
                prepared += 1
        return prepared

    male_prepared   = prepare_gender(MaleCandidate, FemaleCandidate, 'M', 'F')
    female_prepared = prepare_gender(FemaleCandidate, MaleCandidate, 'F', 'M')
    total = male_prepared + female_prepared

    WeeklyBioRun.objects.create(
        run_by=user,
        week_start=week_start,
        week_end=week_end,
        male_processed=MaleCandidate.objects.count(),
        female_processed=FemaleCandidate.objects.count(),
        matches_created=total,
        notes=f"வார இயக்கம் {week_start} முதல் {week_end} வரை. மொத்தம் {total} பொருத்தங்கள்.",
    )
    return total


def _find_matches_inline(exp, receiver_model, sent_ids, qs_age=None):
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
    return list(qs.order_by('-created_at')[:50])


# ─────────────────────────────────────────────
#  WEEKLY SEND PAGE
# ─────────────────────────────────────────────

@login_required
def weekly_send(request):
    from .models import BioSendLog, BioToken, WeeklyBioRun
    from datetime import date, timedelta

    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=days_since_sunday)
    week_key = str(week_start)  # e.g. '2026-03-22'

    # Trigger manual prepare if requested
    if request.method == 'POST' and request.POST.get('action') == 'prepare':
        already_run = WeeklyBioRun.objects.filter(week_start=week_start).exists()
        if already_run:
            messages.error(request, f'இந்த வாரம் ({week_start}) ஏற்கனவே இயக்கப்பட்டது. மீண்டும் இயக்க முடியாது.')
        else:
            try:
                from datetime import timedelta as _td
                week_end_dt = week_start + _td(days=6)
                total = _run_weekly_bios(request.user, week_start, week_end=week_end_dt, week_key=week_key)
                messages.success(request, f'பொருத்தங்கள் தயாரிக்கப்பட்டன. மொத்தம் {total} பொருத்தங்கள்.')
            except Exception as e:
                import traceback
                messages.error(request, f'பிழை: {str(e)} — {traceback.format_exc()[-200:]}')
        return redirect('weekly_send')

    # Get all pending logs grouped by sender using week_key
    male_logs   = _get_sender_summary('M', week_key)
    female_logs = _get_sender_summary('F', week_key)

    already_run_this_week = WeeklyBioRun.objects.filter(week_start=week_start).exists()

    return render(request, 'matrimony/weekly_send.html', {
        'male_logs': male_logs,
        'female_logs': female_logs,
        'month_year': week_key,
        'already_run_this_week': already_run_this_week,
        'week_start': week_start,
    })


def _get_sender_summary(sender_gender, month_year):
    from .models import BioSendLog, BioToken, MaleCandidate, FemaleCandidate
    CandidateModel = MaleCandidate if sender_gender == 'M' else FemaleCandidate
    opposite_gender = 'F' if sender_gender == 'M' else 'M'
    OppModel = FemaleCandidate if sender_gender == 'M' else MaleCandidate

    logs = (BioSendLog.objects
            .filter(sender_gender=sender_gender, month_year=month_year)
            .select_related('bio_token')
            .order_by('sender_id'))

    # Group by sender
    from collections import defaultdict
    sender_map = defaultdict(list)
    for log in logs:
        sender_map[log.sender_id].append(log)

    from datetime import date as _date2
    _today2 = _date2.today()
    result = []
    for sender_id, send_logs in sender_map.items():
        try:
            sender = CandidateModel.objects.get(pk=sender_id)
        except CandidateModel.DoesNotExist:
            continue
        # Skip expired candidates from display
        if sender.premium_end_date and sender.premium_end_date < _today2:
            continue

        pending_logs = [l for l in send_logs if l.status == 'pending']
        sent_count   = len([l for l in send_logs if l.status == 'sent'])
        total_count  = len(send_logs)

        # Build WhatsApp message for pending bios
        wa_message = _build_wa_message(sender, pending_logs, OppModel, opposite_gender)

        pending_log_ids = [str(l.pk) for l in pending_logs]
        result.append({
            'sender': sender,
            'sender_gender': sender_gender,
            'pending_logs': pending_logs,
            'pending_log_ids': ','.join(pending_log_ids),
            'sent_count': sent_count,
            'total_count': total_count,
            'wa_message': wa_message,
            'has_pending': len(pending_logs) > 0,
            'is_warning': False,
        })

    # Also show candidates with NO logs yet — only non-expired ones
    from datetime import date as _date
    _today = _date.today()
    all_senders = CandidateModel.objects.filter(
        whatsapp_number__isnull=False
    ).exclude(whatsapp_number='').filter(
        Q(premium_end_date__isnull=True) | Q(premium_end_date__gte=_today)
    )
    existing_ids = set(sender_map.keys())
    for sender in all_senders:
        if sender.pk not in existing_ids:
            result.append({
                'sender': sender,
                'sender_gender': sender_gender,
                'pending_logs': [],
                'pending_log_ids': '',
                'sent_count': 0,
                'total_count': 0,
                'wa_message': '',
                'has_pending': False,
                'is_warning': False,
            })

    # Show expired candidates at the very bottom with warning highlight
    expired_senders = CandidateModel.objects.filter(
        whatsapp_number__isnull=False
    ).exclude(whatsapp_number='').filter(
        premium_end_date__lt=_today
    )
    for sender in expired_senders:
        result.append({
            'sender': sender,
            'sender_gender': sender_gender,
            'pending_logs': [],
            'pending_log_ids': '',
            'sent_count': 0,
            'total_count': 0,
            'wa_message': '',
            'has_pending': False,
            'is_warning': True,
            'warning_reason': 'காலாவதியான பிரீமியம்',
        })

    return result


def _build_wa_message(sender, pending_logs, OppModel, opp_gender):
    from .models import BioToken
    from django.conf import settings
    base_url = getattr(settings, 'SITE_URL', 'https://sembodai-production.up.railway.app')

    if not pending_logs:
        return ''

    lines = [f"வணக்கம் {sender.name},\n\nசெம்போடையார் வன்னியர் திருமண மையம்\nஇந்த வார பொருத்தமான வரன்கள்:\n"]
    for i, log in enumerate(pending_logs, 1):
        try:
            receiver = OppModel.objects.get(pk=log.receiver_id)
        except OppModel.DoesNotExist:
            continue
        # Create token only if missing — never replace existing valid token
        from .models import BioToken
        if not log.bio_token:
            token_obj = BioToken.create_for_candidate(opp_gender, log.receiver_id)
            log.bio_token = token_obj
            log.save(update_fields=['bio_token'])
        token = log.bio_token.token
        bio_url = f"{base_url}/bio/{token}/"
        age_str = f"{receiver.age} வயது" if receiver.age else ''
        lines.append(f"{i}. {receiver.name}{', ' + age_str if age_str else ''}")
        lines.append(f"   👉 {bio_url}")
        lines.append("")

    lines.append("- செம்போடையார் வன்னியர் திருமண மையம்")
    return "\n".join(lines)


@login_required
def mark_sent(request, log_ids):
    """Mark multiple BioSendLog entries as sent"""
    from .models import BioSendLog
    from django.utils import timezone
    if request.method == 'POST':
        try:
            ids = [int(x.strip()) for x in str(log_ids).split(',') if x.strip().isdigit()]
            if ids:
                BioSendLog.objects.filter(pk__in=ids, status='pending').update(
                    status='sent',
                    sent_at=timezone.now(),
                )
                messages.success(request, f'{len(ids)} பயோ அனுப்பியதாக குறிக்கப்பட்டது.')
        except Exception as e:
            messages.error(request, f'பிழை: {str(e)}')
    return redirect('weekly_send')


# ─────────────────────────────────────────────
#  PUBLIC BIO VIEW  (no login required)
# ─────────────────────────────────────────────

def public_bio_view(request, token):
    from .models import BioToken, FamilyMember
    from django.utils import timezone

    try:
        bio_token = BioToken.objects.get(token=token)
    except BioToken.DoesNotExist:
        from django.http import Http404
        raise Http404("இந்த இணைப்பு செல்லாது.")

    if bio_token.is_expired:
        return render(request, 'matrimony/bio_expired.html')

    gender = bio_token.candidate_gender
    candidate_id = bio_token.candidate_id

    if gender == 'M':
        from .models import MaleCandidate
        candidate = get_object_or_404(MaleCandidate, pk=candidate_id)
    else:
        from .models import FemaleCandidate
        candidate = get_object_or_404(FemaleCandidate, pk=candidate_id)

    family_members = FamilyMember.objects.filter(
        candidate_gender=gender, candidate_id=candidate_id
    )
    jathagam_map = candidate.get_jathagam_map()

    # Load admin_profile from the user who added this candidate
    admin_profile = None
    if candidate.created_by:
        try:
            admin_profile = candidate.created_by.adminprofile
        except Exception:
            pass

    # Use existing print template but without address
    return render(request, 'matrimony/candidate_print.html', {
        'candidate': candidate,
        'admin_profile': admin_profile,
        'photo_base64': None,
        'gender': gender,
        'family_members': family_members,
        'jathagam_map': jathagam_map,
        'is_public': True,  # hides address in template
    })


# ─────────────────────────────────────────────
#  EXPECTATION SAVE  (AJAX from candidate form)
# ─────────────────────────────────────────────

@login_required
def save_expectation(request, gender, pk):
    from .models import (CandidateExpectation, ExpectationNachathiram,
                          ExpectationSubCaste, ExpectationDistrict,
                          ExpectationProfession, ExpectationComplexion)
    if request.method != 'POST':
        return redirect('candidate_edit', gender=gender, pk=pk)

    exp, _ = CandidateExpectation.objects.get_or_create(
        candidate_gender=gender,
        candidate_id=pk,
    )

    exp.age_min           = request.POST.get('exp_age_min') or None
    exp.age_max           = request.POST.get('exp_age_max') or None
    exp.salary_min        = request.POST.get('exp_salary_min') or None
    exp.education_min     = request.POST.get('exp_education_min', '').strip()
    exp.job_type          = request.POST.get('exp_job_type', 'any')
    exp.notes             = request.POST.get('exp_notes', '').strip()

    hmin = request.POST.get('exp_height_min')
    hmax = request.POST.get('exp_height_max')
    sev  = request.POST.get('exp_sevadosham_ok')
    own  = request.POST.get('exp_own_house_pref')
    mar  = request.POST.get('exp_marital_status_ok')

    from .models import Height, Sevadosham, OwnHouse, MaritalStatus
    exp.sevadosham_ok     = Sevadosham.objects.filter(pk=sev).first() if sev else None
    exp.own_house_pref    = OwnHouse.objects.filter(pk=own).first() if own else None
    exp.marital_status_ok = MaritalStatus.objects.filter(pk=mar).first() if mar else None
    exp.save()

    # Save many-to-many
    exp.nachathirams.all().delete()
    for nid in request.POST.getlist('exp_nachathirams[]'):
        from .models import Nachathiram
        n = Nachathiram.objects.filter(pk=nid).first()
        if n: ExpectationNachathiram.objects.create(expectation=exp, nachathiram=n)

    exp.sub_castes.all().delete()
    for sid in request.POST.getlist('exp_sub_castes[]'):
        from .models import SubCaste
        s = SubCaste.objects.filter(pk=sid).first()
        if s: ExpectationSubCaste.objects.create(expectation=exp, sub_caste=s)

    exp.districts.all().delete()
    for did in request.POST.getlist('exp_districts[]'):
        from .models import District
        d = District.objects.filter(pk=did).first()
        if d: ExpectationDistrict.objects.create(expectation=exp, district=d)

    exp.professions.all().delete()
    for pid in request.POST.getlist('exp_professions[]'):
        from .models import Profession
        p = Profession.objects.filter(pk=pid).first()
        if p: ExpectationProfession.objects.create(expectation=exp, profession=p)

    exp.complexions.all().delete()
    for cid in request.POST.getlist('exp_complexions[]'):
        from .models import Complexion
        c = Complexion.objects.filter(pk=cid).first()
        if c: ExpectationComplexion.objects.create(expectation=exp, complexion=c)

    messages.success(request, 'எதிர்பார்ப்பு சேமிக்கப்பட்டது.')
    return redirect('candidate_detail', gender=gender, pk=pk)


@login_required  
def cron_prepare_bios(request):
    """Internal endpoint — triggered by Railway cron via curl"""
    from django.core.management import call_command
    from django.http import HttpResponse
    # Verify secret token to prevent unauthorized access
    from django.conf import settings
    token = request.GET.get('token', '')
    cron_secret = getattr(settings, 'CRON_SECRET', '')
    if not cron_secret or token != cron_secret:
        return HttpResponse('Unauthorized', status=401)
    call_command('prepare_weekly_bios')
    return HttpResponse('OK', status=200)


# ─────────────────────────────────────────────
#  BIO SEND HISTORY PAGE
# ─────────────────────────────────────────────

@login_required
def bio_history(request):
    from .models import BioSendLog, BioToken, MaleCandidate, FemaleCandidate
    from django.utils import timezone

    # Delete log entry (superuser only)
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        if request.user.is_superuser:
            log_id = request.POST.get('log_id')
            try:
                BioSendLog.objects.filter(pk=log_id).delete()
                messages.success(request, 'பதிவு நீக்கப்பட்டது.')
            except Exception as e:
                messages.error(request, f'பிழை: {str(e)}')
        else:
            messages.error(request, 'அனுமதி இல்லை.')
        return redirect(request.get_full_path())

    gender   = request.GET.get('gender', 'M')
    search   = request.GET.get('search', '').strip()
    month    = request.GET.get('month', '')
    status   = request.GET.get('status', '')
    page_num = request.GET.get('page', 1)

    qs = BioSendLog.objects.select_related('bio_token').filter(sender_gender=gender)

    if month:
        qs = qs.filter(month_year=month)
    if status:
        qs = qs.filter(status=status)

    # Search by sender UID
    if search:
        CandidateModel = MaleCandidate if gender == 'M' else FemaleCandidate
        matched_ids = list(
            CandidateModel.objects.filter(uid__icontains=search)
            .values_list('pk', flat=True)
        )
        qs = qs.filter(sender_id__in=matched_ids)

    qs = qs.order_by('-prepared_at')

    from django.core.paginator import Paginator
    paginator = Paginator(qs, 50)
    page_obj  = paginator.get_page(page_num)

    # Enrich each log with sender/receiver names and token expiry
    CandidateM = MaleCandidate
    CandidateF = FemaleCandidate
    now = timezone.now()

    rows = []
    for log in page_obj:
        # Sender
        try:
            SenderModel = CandidateM if log.sender_gender == 'M' else CandidateF
            sender = SenderModel.objects.get(pk=log.sender_id)
            sender_uid  = sender.uid
            sender_name = sender.name
        except Exception:
            sender_uid  = f"{log.sender_gender}{log.sender_id}"
            sender_name = '-'

        # Receiver
        try:
            ReceiverModel = CandidateM if log.receiver_gender == 'M' else CandidateF
            receiver = ReceiverModel.objects.get(pk=log.receiver_id)
            receiver_uid  = receiver.uid
            receiver_name = receiver.name
        except Exception:
            receiver_uid  = f"{log.receiver_gender}{log.receiver_id}"
            receiver_name = '-'

        # Token info
        token_str    = log.bio_token.token[:16] + '...' if log.bio_token else '-'
        expires_at   = log.bio_token.expires_at if log.bio_token else None
        is_expired   = (expires_at and now > expires_at)
        bio_url      = f"/bio/{log.bio_token.token}/" if log.bio_token else ''

        rows.append({
            'log':           log,
            'sender_uid':    sender_uid,
            'sender_name':   sender_name,
            'receiver_uid':  receiver_uid,
            'receiver_name': receiver_name,
            'token_short':   token_str,
            'expires_at':    expires_at,
            'is_expired':    is_expired,
            'bio_url':       bio_url,
        })

    # Get distinct months for filter dropdown
    months = (BioSendLog.objects
              .filter(sender_gender=gender)
              .values_list('month_year', flat=True)
              .distinct()
              .order_by('-month_year'))

    return render(request, 'matrimony/bio_history.html', {
        'rows':     rows,
        'page_obj': page_obj,
        'gender':   gender,
        'search':   search,
        'month':    month,
        'status':   status,
        'months':   months,
        'total':    paginator.count,
    })


# ─────────────────────────────────────────────
#  WEEKLY RUN LOG PAGE (superuser only)
# ─────────────────────────────────────────────

@login_required
def weekly_run_log(request):
    from django.http import HttpResponseForbidden
    if not request.user.is_superuser:
        return HttpResponseForbidden("அனுமதி இல்லை")
    from .models import WeeklyBioRun
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        run_id = request.POST.get('run_id')
        try:
            WeeklyBioRun.objects.filter(pk=run_id).delete()
            messages.success(request, 'இயக்க பதிவு நீக்கப்பட்டது. இப்போது மீண்டும் இயக்கலாம்.')
        except Exception as e:
            messages.error(request, f'பிழை: {str(e)}')
        return redirect('weekly_run_log')
    runs = WeeklyBioRun.objects.select_related('run_by').all()
    return render(request, 'matrimony/weekly_run_log.html', {'runs': runs})


# ─────────────────────────────────────────────
#  MEDIA FILES PAGE (superuser only)
# ─────────────────────────────────────────────

@login_required
def media_files(request):
    from django.http import HttpResponseForbidden
    if not request.user.is_superuser:
        return HttpResponseForbidden("அனுமதி இல்லை")

    from .models import CandidatePhoto, MaleCandidate, FemaleCandidate
    import os
    from django.conf import settings

    # Handle delete
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        photo_id = request.POST.get('photo_id')
        try:
            photo = CandidatePhoto.objects.get(pk=photo_id)
            if photo.photo and os.path.isfile(photo.photo.path):
                os.remove(photo.photo.path)
            photo.delete()
            messages.success(request, 'புகைப்படம் நீக்கப்பட்டது.')
        except CandidatePhoto.DoesNotExist:
            messages.error(request, 'புகைப்படம் கிடைக்கவில்லை.')
        return redirect('media_files')

    # Get all photos from DB
    photos = CandidatePhoto.objects.select_related(
        'male_candidate', 'female_candidate'
    ).order_by('-uploaded_at')

    rows = []
    total_size = 0
    for photo in photos:
        candidate = photo.male_candidate or photo.female_candidate
        gender = 'M' if photo.male_candidate else 'F'
        file_size = 0
        file_exists = False
        try:
            if photo.photo and os.path.isfile(photo.photo.path):
                file_size = os.path.getsize(photo.photo.path)
                file_exists = True
                total_size += file_size
        except Exception:
            pass

        rows.append({
            'photo': photo,
            'candidate': candidate,
            'gender': gender,
            'uid': candidate.uid if candidate else '-',
            'name': candidate.name if candidate else '-',
            'filename': os.path.basename(photo.photo.name) if photo.photo else '-',
            'file_size': file_size,
            'file_size_kb': round(file_size / 1024, 1),
            'file_exists': file_exists,
            'uploaded_at': photo.uploaded_at,
        })

    # Also scan for orphan files on disk not in DB
    db_files = set(p.photo.name for p in photos if p.photo)
    orphan_files = []
    photos_dir = os.path.join(settings.MEDIA_ROOT, 'photos')
    if os.path.isdir(photos_dir):
        for fname in os.listdir(photos_dir):
            fpath = f'photos/{fname}'
            if fpath not in db_files:
                full_path = os.path.join(photos_dir, fname)
                fsize = os.path.getsize(full_path)
                total_size += fsize
                orphan_files.append({
                    'filename': fname,
                    'file_size_kb': round(fsize / 1024, 1),
                    'full_path': full_path,
                })

    total_size_mb = round(total_size / (1024 * 1024), 2)

    return render(request, 'matrimony/media_files.html', {
        'rows': rows,
        'orphan_files': orphan_files,
        'total_count': len(rows),
        'orphan_count': len(orphan_files),
        'total_size_mb': total_size_mb,
    })


@login_required
def media_delete_orphan(request):
    from django.http import HttpResponseForbidden
    if not request.user.is_superuser:
        return HttpResponseForbidden("அனுமதி இல்லை")
    import os
    from django.conf import settings
    if request.method == 'POST':
        filename = request.POST.get('filename')
        if filename and '/' not in filename and '..' not in filename:
            full_path = os.path.join(settings.MEDIA_ROOT, 'photos', filename)
            if os.path.isfile(full_path):
                os.remove(full_path)
                messages.success(request, f'{filename} நீக்கப்பட்டது.')
    return redirect('media_files')
