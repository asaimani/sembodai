from django.db import models
from django.contrib.auth.models import User
import uuid


class State(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name = "மாநிலம்"; ordering = ['name']

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name = "மாவட்டம்"; ordering = ['name']

class Rasi(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name
    class Meta: verbose_name = "ராசி"

class Nachathiram(models.Model):
    name = models.CharField(max_length=50)
    rasi = models.ForeignKey(Rasi, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return self.name
    class Meta: verbose_name = "நட்சத்திரம்"

class Profession(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name = "தொழில்"

class Jathagam(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name = "ஜாதகம்"


# South Indian Horoscope Chart - 12 house planet positions
PLANET_CHOICES = [
    ('', '-'),
    ('லக்னம்', 'லக்னம்'),
    ('சூ', 'சூரியன் (சூ)'),
    ('ச', 'சந்திரன் (ச)'),
    ('செ', 'செவ்வாய் (செ)'),
    ('பு', 'புதன் (பு)'),
    ('கு', 'குரு (கு)'),
    ('சுக்', 'சுக்கிரன் (சுக்)'),
    ('சனி', 'சனி'),
    ('ரா', 'ராகு (ரா)'),
    ('கே', 'கேது (கே)'),
    ('லக்,சூ', 'லக்னம் + சூரியன்'),
    ('லக்,ச', 'லக்னம் + சந்திரன்'),
    ('லக்,செ', 'லக்னம் + செவ்வாய்'),
    ('லக்,பு', 'லக்னம் + புதன்'),
    ('லக்,கு', 'லக்னம் + குரு'),
    ('லக்,சுக்', 'லக்னம் + சுக்கிரன்'),
    ('லக்,சனி', 'லக்னம் + சனி'),
    ('சூ,ச', 'சூரியன் + சந்திரன்'),
    ('சூ,செ', 'சூரியன் + செவ்வாய்'),
    ('சூ,பு', 'சூரியன் + புதன்'),
    ('சூ,கு', 'சூரியன் + குரு'),
    ('சூ,சனி', 'சூரியன் + சனி'),
    ('ச,செ', 'சந்திரன் + செவ்வாய்'),
    ('ச,கு', 'சந்திரன் + குரு'),
    ('ச,சனி', 'சந்திரன் + சனி'),
    ('செ,கு', 'செவ்வாய் + குரு'),
    ('செ,சனி', 'செவ்வாய் + சனி'),
    ('பு,சுக்', 'புதன் + சுக்கிரன்'),
    ('கு,சனி', 'குரு + சனி'),
    ('ரா,கே', 'ராகு + கேது'),
]

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, verbose_name="இருப்பிடம்")
    address = models.TextField(verbose_name="முகவரி")
    phone = models.CharField(max_length=15, verbose_name="தொலைபேசி")
    def __str__(self): return f"{self.user.get_full_name()} - {self.location}"


GENDER_CHOICES = [('M', 'ஆண்'), ('F', 'பெண்')]
STATUS_CHOICES = [('active', 'செயலில்'), ('inactive', 'செயலற்று')]
SEVADOSHAM_CHOICES = [('yes', 'உண்டு'), ('no', 'இல்லை'), ('partial', 'பாதி')]

def generate_uid(gender):
    prefix = 'M' if gender == 'M' else 'F'
    return f"{prefix}{str(uuid.uuid4().int)[:6]}"


class Candidate(models.Model):
    uid = models.CharField(max_length=20, unique=True, editable=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="பாலினம்")
    name = models.CharField(max_length=200, verbose_name="பெயர்")
    date_of_birth = models.DateField(verbose_name="பிறந்த தேதி")
    rasi = models.ForeignKey(Rasi, on_delete=models.SET_NULL, null=True, verbose_name="ராசி")
    nachathiram = models.ForeignKey(Nachathiram, on_delete=models.SET_NULL, null=True, verbose_name="நட்சத்திரம்")
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, verbose_name="தொழில்")
    profession_comments = models.TextField(blank=True, verbose_name="தொழில் விவரம்")
    educational_qualification = models.CharField(max_length=200, verbose_name="கல்வித் தகுதி")
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="வருடாந்திர வருமானம்")
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="மாத சம்பளம்")
    height = models.CharField(max_length=20, verbose_name="உயரம்")
    caste = models.CharField(max_length=100, verbose_name="சாதி")
    sub_caste = models.CharField(max_length=100, blank=True, verbose_name="உட்சாதி")
    sevadosham = models.CharField(max_length=10, choices=SEVADOSHAM_CHOICES, verbose_name="செவ்வாய் தோஷம்")
    ragu_kethu = models.CharField(max_length=50, blank=True, verbose_name="ராகு/கேது")
    property_value = models.CharField(max_length=200, blank=True, verbose_name="சொத்து மதிப்பு")
    jathagam = models.ForeignKey(Jathagam, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ஜாதகம்")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, verbose_name="மாநிலம்")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name="மாவட்டம்")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="நிலை")
    premium_start_date = models.DateField(null=True, blank=True, verbose_name="பிரீமியம் தொடக்க தேதி")
    premium_end_date = models.DateField(null=True, blank=True, verbose_name="பிரீமியம் முடிவு தேதி")
    is_paid = models.BooleanField(default=True, verbose_name="கட்டணம் செலுத்தியது")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='candidates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_new = models.BooleanField(default=True)

    # Jathagam Chart - 12 Houses (South Indian Square Format)
    jathagam_h1  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 1 (லக்னம்)")
    jathagam_h2  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 2")
    jathagam_h3  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 3")
    jathagam_h4  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 4")
    jathagam_h5  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 5")
    jathagam_h6  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 6")
    jathagam_h7  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 7")
    jathagam_h8  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 8")
    jathagam_h9  = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 9")
    jathagam_h10 = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 10")
    jathagam_h11 = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 11")
    jathagam_h12 = models.CharField(max_length=50, blank=True, choices=PLANET_CHOICES, verbose_name="வீடு 12")

    # Father info
    father_name = models.CharField(max_length=200, blank=True, verbose_name="தந்தை பெயர்")
    father_profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True, related_name='fathers', verbose_name="தந்தை தொழில்")
    # Mother info
    mother_name = models.CharField(max_length=200, blank=True, verbose_name="தாய் பெயர்")
    mother_profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True, related_name='mothers', verbose_name="தாய் தொழில்")
    # Siblings
    siblings_info = models.TextField(blank=True, verbose_name="உடன்பிறந்தோர் விவரம்")

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = generate_uid(self.gender)
        super().save(*args, **kwargs)

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def is_premium_expired(self):
        from datetime import date
        if self.premium_end_date:
            return self.premium_end_date < date.today()
        return False

    def __str__(self): return f"{self.uid} - {self.name}"
    class Meta: verbose_name = "விண்ணப்பதாரர்"; ordering = ['-created_at']


def candidate_photo_path(instance, filename):
    import os
    ext = os.path.splitext(filename)[1].lower()
    # Folder based on gender
    folder = 'male' if instance.candidate.gender == 'M' else 'female'
    # Count existing photos to get sequence number
    existing = CandidatePhoto.objects.filter(candidate=instance.candidate).count()
    seq = str(existing + 1).zfill(2)
    return f'photos/{folder}/{instance.candidate.uid}_{seq}{ext}'


class CandidatePhoto(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=candidate_photo_path)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta: verbose_name = "புகைப்படம்"


class ShadowCandidate(models.Model):
    """Unpaid candidate data stored separately"""
    original_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    class Meta: verbose_name = "நிலுவை விண்ணப்பம்"
