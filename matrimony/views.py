from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
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
    yesterday = today - timedelta(days=1)
    new_entries = Candidate.objects.filter(created_at__date=today, is_paid=True)
    expired = Candidate.objects.filter(premium_end_date__lt=today, is_paid=True, status='active')
    male_count = Candidate.objects.filter(gender='M', is_paid=True).count()
    female_count = Candidate.objects.filter(gender='F', is_paid=True).count()
    total = Candidate.objects.filter(is_paid=True).count()
    context = {
        'new_entries': new_entries,
        'expired_entries': expired,
        'male_count': male_count,
        'female_count': female_count,
        'total': total,
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
    status = request.GET.get('status', 'active')

    candidates = Candidate.objects.filter(is_paid=True).select_related('rasi', 'nachathiram', 'profession', 'state', 'district')

    if gender:
        candidates = candidates.filter(gender=gender)
    if search:
        candidates = candidates.filter(Q(name__icontains=search) | Q(uid__icontains=search))
    if rasi_id:
        candidates = candidates.filter(rasi_id=rasi_id)
    if nachathiram_id:
        candidates = candidates.filter(nachathiram_id=nachathiram_id)
    if salary_min:
        candidates = candidates.filter(monthly_salary__gte=salary_min)
    if status:
        candidates = candidates.filter(status=status)
    if age_min:
        max_dob = date(date.today().year - int(age_min), date.today().month, date.today().day)
        candidates = candidates.filter(date_of_birth__lte=max_dob)
    if age_max:
        min_dob = date(date.today().year - int(age_max), date.today().month, date.today().day)
        candidates = candidates.filter(date_of_birth__gte=min_dob)

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


@login_required
def candidate_add(request):
    gender = request.GET.get('gender', 'M')
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        photos = request.FILES.getlist('photos')
        is_paid = request.POST.get('is_paid', 'true') == 'true'

        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.created_by = request.user
            candidate.is_paid = is_paid

            if not is_paid:
                shadow = ShadowCandidate(original_data=request.POST.dict(), notes="கட்டணம் செலுத்தாத விண்ணப்பம்")
                shadow.save()
                messages.warning(request, 'விண்ணப்பம் நிலுவை பட்டியலில் சேர்க்கப்பட்டது.')
                return redirect('candidate_list')

            candidate.save()
            for i, photo in enumerate(photos[:3]):
                CandidatePhoto.objects.create(candidate=candidate, photo=photo, is_primary=(i == 0))
            messages.success(request, f'விண்ணப்பம் வெற்றிகரமாக சேர்க்கப்பட்டது. UID: {candidate.uid}')
            return redirect('candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm(initial={'gender': gender})

    return render(request, 'matrimony/candidate_form.html', {'form': form, 'gender': gender, 'title': 'புதிய விண்ணப்பம்'})


@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    return render(request, 'matrimony/candidate_detail.html', {'candidate': candidate})


@login_required
def candidate_edit(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            photos = request.FILES.getlist('photos')
            existing_count = candidate.photos.count()
            for photo in photos[:max(0, 3 - existing_count)]:
                CandidatePhoto.objects.create(candidate=candidate, photo=photo)
            messages.success(request, 'விண்ணப்பம் புதுப்பிக்கப்பட்டது.')
            return redirect('candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'matrimony/candidate_form.html', {'form': form, 'candidate': candidate, 'title': 'திருத்து'})


@login_required
def candidate_print(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    admin_profile = None
    try:
        admin_profile = request.user.adminprofile
    except:
        pass
    return render(request, 'matrimony/candidate_print.html', {'candidate': candidate, 'admin_profile': admin_profile})


@login_required
def shadow_list(request):
    shadows = ShadowCandidate.objects.all().order_by('-created_at')
    return render(request, 'matrimony/shadow_list.html', {'shadows': shadows})


def get_nachathirams(request):
    rasi_id = request.GET.get('rasi_id')
    nachathirams = Nachathiram.objects.filter(rasi_id=rasi_id).values('id', 'name')
    return JsonResponse(list(nachathirams), safe=False)
