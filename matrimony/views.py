from django.shortcuts import render, redirect, get_object_or_404
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
    new_male = MaleCandidate.objects.filter(created_at__date=today, is_paid=True)
    new_female = FemaleCandidate.objects.filter(created_at__date=today, is_paid=True)
    expired_male = MaleCandidate.objects.filter(premium_end_date__lt=today, is_paid=True, status__code='active')
    expired_female = FemaleCandidate.objects.filter(premium_end_date__lt=today, is_paid=True, status__code='active')
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
    status_filter = request.GET.get('status', 'active')

    def apply_filters(qs):
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(uid__icontains=search))
        if rasi_id:
            qs = qs.filter(rasi_id=rasi_id)
        if nachathiram_id:
            qs = qs.filter(nachathiram_id=nachathiram_id)
        if salary_min:
            qs = qs.filter(monthly_salary__gte=salary_min)
        if status_filter:
            qs = qs.filter(status__code=status_filter)
        if age_min:
            max_dob = date(date.today().year - int(age_min), date.today().month, date.today().day)
            qs = qs.filter(date_of_birth__lte=max_dob)
        if age_max:
            min_dob = date(date.today().year - int(age_max), date.today().month, date.today().day)
            qs = qs.filter(date_of_birth__gte=min_dob)
        return qs

    males = apply_filters(MaleCandidate.objects.filter(is_paid=True).select_related('rasi', 'nachathiram', 'profession', 'state', 'district'))
    females = apply_filters(FemaleCandidate.objects.filter(is_paid=True).select_related('rasi', 'nachathiram', 'profession', 'state', 'district'))

    if gender == 'M':
        candidates = [('M', c) for c in males]
    elif gender == 'F':
        candidates = [('F', c) for c in females]
    else:
        candidates = [('M', c) for c in males] + [('F', c) for c in females]
        candidates.sort(key=lambda x: x[1].created_at, reverse=True)

    rasis = Rasi.objects.all()
    nachathirams = Nachathiram.objects.all()
    context = {
        'candidates': candidates,
        'rasis': rasis,
        'nachathirams': nachathirams,
        'gender': gender,
        'search': search,
    }
    return render(request, 'matrimony/candidate_list.html', context)


def _save_jathagam(candidate, post_data):
    from .models import Planet
    for prefix in ['rasi', 'navamsam']:
        for i in range(1, 13):
            fname = f'{prefix}_h{i}'
            field_id = f'{prefix}_h{i}_id'
            val = post_data.get(fname, '')
            if val:
                try:
                    planet = Planet.objects.get(pk=int(val))
                    setattr(candidate, fname, planet)
                except (Planet.DoesNotExist, ValueError):
                    setattr(candidate, fname, None)
            else:
                setattr(candidate, fname, None)
    candidate.save()


def _save_photos(candidate, files, is_male):
    for i, photo in enumerate(files[:3]):
        if is_male:
            CandidatePhoto.objects.create(male_candidate=candidate, photo=photo, is_primary=(i == 0))
        else:
            CandidatePhoto.objects.create(female_candidate=candidate, photo=photo, is_primary=(i == 0))


@login_required
def candidate_add(request):
    gender = request.GET.get('gender', 'M')
    is_male = gender == 'M'
    FormClass = MaleCandidateForm if is_male else FemaleCandidateForm

    if request.method == 'POST':
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

            candidate.save()
            _save_jathagam(candidate, request.POST)
            _save_photos(candidate, photos, is_male)
            messages.success(request, f'விண்ணப்பம் வெற்றிகரமாக சேர்க்கப்பட்டது. UID: {candidate.uid}')
            return redirect('candidate_detail', gender=gender, pk=candidate.pk)
    else:
        form = FormClass()

    from .models import Planet
    return render(request, 'matrimony/candidate_form.html', {
        'form': form, 'gender': gender,
        'title': 'புதிய விண்ணப்பம்',
        'planets': Planet.objects.all(),
    })


def _get_candidate(gender, pk):
    if gender == 'M':
        return get_object_or_404(MaleCandidate, pk=pk)
    return get_object_or_404(FemaleCandidate, pk=pk)


@login_required
def candidate_detail(request, gender, pk):
    candidate = _get_candidate(gender, pk)
    return render(request, 'matrimony/candidate_detail.html', {'candidate': candidate, 'gender': gender})


@login_required
def candidate_edit(request, gender, pk):
    candidate = _get_candidate(gender, pk)
    is_male = gender == 'M'
    FormClass = MaleCandidateForm if is_male else FemaleCandidateForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            photos = request.FILES.getlist('photos')
            existing_count = candidate.photos.count()
            _save_photos(candidate, photos[:max(0, 3 - existing_count)], is_male)
            _save_jathagam(candidate, request.POST)
            messages.success(request, 'விண்ணப்பம் புதுப்பிக்கப்பட்டது.')
            return redirect('candidate_detail', gender=gender, pk=candidate.pk)
    else:
        form = FormClass(instance=candidate)

    from .models import Planet
    return render(request, 'matrimony/candidate_form.html', {
        'form': form, 'candidate': candidate, 'gender': gender,
        'title': 'திருத்து',
        'planets': Planet.objects.all(),
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

    return render(request, 'matrimony/candidate_print.html', {
        'candidate': candidate,
        'admin_profile': admin_profile,
        'photo_base64': photo_base64,
        'gender': gender,
    })


@login_required
def shadow_list(request):
    shadows = ShadowCandidate.objects.all().order_by('-created_at')
    return render(request, 'matrimony/shadow_list.html', {'shadows': shadows})


@login_required
def delete_photo(request, photo_id):
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


def get_nachathirams(request):
    rasi_id = request.GET.get('rasi_id')
    nachathirams = Nachathiram.objects.filter(rasi_id=rasi_id).values('id', 'name')
    return JsonResponse(list(nachathirams), safe=False)
