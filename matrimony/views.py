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
    male_count = MaleCandidate.objects.filter(is_paid=True).count()
    female_count = FemaleCandidate.objects.filter(is_paid=True).count()
    total = male_count + female_count
    new_male = MaleCandidate.objects.filter(created_at__date=today, is_paid=True).order_by('-created_at')[:20]
    new_female = FemaleCandidate.objects.filter(created_at__date=today, is_paid=True).order_by('-created_at')[:20]
    expired_male = MaleCandidate.objects.filter(premium_end_date__lt=today, is_paid=True, status__code='active').order_by('-premium_end_date')[:20]
    expired_female = FemaleCandidate.objects.filter(premium_end_date__lt=today, is_paid=True, status__code='active').order_by('-premium_end_date')[:20]
    context = {
        'male_count': male_count,
        'female_count': female_count,
        'total': total,
        'new_entries': list(new_male) + list(new_female),
        'expired_entries': list(expired_male) + list(expired_female),
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

    base_select = {'select_related': ['rasi', 'nachathiram', 'profession', 'state', 'district']}

    if gender == 'M':
        qs = apply_filters(
            MaleCandidate.objects.filter(is_paid=True)
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        # Wrap with gender tag using values + annotate approach via iterator
        paginator = Paginator(qs, PER_PAGE)
        page_obj = paginator.get_page(page_num)
        candidates = [('M', c) for c in page_obj]
        total_count = paginator.count

    elif gender == 'F':
        qs = apply_filters(
            FemaleCandidate.objects.filter(is_paid=True)
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        paginator = Paginator(qs, PER_PAGE)
        page_obj = paginator.get_page(page_num)
        candidates = [('F', c) for c in page_obj]
        total_count = paginator.count

    else:
        # Both genders: paginate males and females separately, interleave by created_at
        # To avoid in-memory sort of 2M rows, paginate each independently
        # and show them as two separate sorted querysets using DB ordering
        males_qs = apply_filters(
            MaleCandidate.objects.filter(is_paid=True)
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        females_qs = apply_filters(
            FemaleCandidate.objects.filter(is_paid=True)
            .select_related(*base_select['select_related'])
            .order_by('-created_at')
        )
        # Combine using slicing — DB does the heavy lifting, no Python sort
        male_count = males_qs.count()
        female_count = females_qs.count()
        total_count = male_count + female_count

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
    context = {
        'candidates': candidates,
        'page_obj': page_obj,
        'total_count': total_count,
        'rasis': rasis,
        'nachathirams': nachathirams,
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
        is_paid = request.POST.get('is_paid', 'true') == 'true'

        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.created_by = request.user
            candidate.is_paid = is_paid

            if not is_paid:
                ShadowCandidate.objects.create(original_data=request.POST.dict(), notes="கட்டணம் செலுத்தாத விண்ணப்பம்")
                messages.warning(request, 'விண்ணப்பம் நிலுவை பட்டியலில் சேர்க்கப்பட்டது.')
                return redirect('candidate_list')

            # Always force active status if form submitted with active or empty
            from .models import CandidateStatus
            status_id = request.POST.get('status', '')
            if status_id:
                try:
                    candidate.status = CandidateStatus.objects.get(pk=int(status_id))
                except Exception:
                    pass
            if not candidate.status_id:
                active_status = CandidateStatus.objects.filter(code='active').first()
                if active_status:
                    candidate.status = active_status
            candidate.save()
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

    from .models import Planet, Relation, MaritalStatus
    empty_map = {'R': {h: '' for h in range(1, 13)}, 'N': {h: '' for h in range(1, 13)}}
    return render(request, 'matrimony/candidate_form.html', {
        'form': form, 'gender': gender,
        'title': 'புதிய விண்ணப்பம்',
        'planets': Planet.objects.all(),
        'relations': Relation.objects.all(),
        'marital_statuses': MaritalStatus.objects.all(),
        'family_members': [],
        'jathagam_map': empty_map,
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
                active = CandidateStatus.objects.filter(code='active').first()
                if active:
                    saved.status = active
            saved.save()
            form.save_m2m()
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

    from .models import Planet, Relation, MaritalStatus
    gender_code = 'M' if is_male else 'F'
    family_members = list(FamilyMember.objects.filter(candidate_gender=gender_code, candidate_id=candidate.pk))
    jathagam_map = candidate.get_jathagam_map()
    return render(request, 'matrimony/candidate_form.html', {
        'form': form, 'candidate': candidate, 'gender': gender,
        'title': 'திருத்து',
        'planets': Planet.objects.all(),
        'relations': Relation.objects.all(),
        'marital_statuses': MaritalStatus.objects.all(),
        'family_members': family_members,
        'jathagam_map': jathagam_map,
    })


@login_required
def candidate_print(request, gender, pk):
    import base64, os
    candidate = _get_candidate(gender, pk)
    admin_profile = None
    try:
        admin_profile = request.user.adminprofile
    except:
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
    return render(request, 'matrimony/candidate_print.html', {
        'candidate': candidate,
        'admin_profile': admin_profile,
        'photo_base64': photo_base64,
        'gender': gender,
        'family_members': family_members,
        'jathagam_map': jathagam_map,
    })


@login_required
def shadow_list(request):
    shadows = ShadowCandidate.objects.all().order_by('-created_at')
    return render(request, 'matrimony/shadow_list.html', {'shadows': shadows})



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
