from django.db import models
from django.contrib.auth.models import User
import uuid


# ─────────────────────────────────────────────
#  LOOKUP TABLES  (all editable via admin)
# ─────────────────────────────────────────────

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
    class Meta: verbose_name = "ராசி"; ordering = ['id']

class Nachathiram(models.Model):
    name = models.CharField(max_length=50)
    rasi = models.ForeignKey(Rasi, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return self.name
    class Meta: verbose_name = "நட்சத்திரம்"; ordering = ['id']

class Profession(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name = "தொழில்"; ordering = ['name']

class JathagamType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name = "ஜாதகம் வகை"; ordering = ['name']

class Planet(models.Model):
    """Lookup table for Jathagam house dropdown values"""
    code  = models.CharField(max_length=20, unique=True, verbose_name="குறியீடு")  # e.g. சூ
    name  = models.CharField(max_length=100, verbose_name="பெயர்")                 # e.g. சூரியன் (சூ)
    order = models.PositiveIntegerField(default=0, verbose_name="வரிசை")
    def __str__(self): return self.name
    class Meta: verbose_name = "கோள்"; ordering = ['order', 'id']

class Sevadosham(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="குறியீடு")
    name = models.CharField(max_length=100, verbose_name="பெயர்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "செவ்வாய் தோஷம்"; ordering = ['order']

class CandidateStatus(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="குறியீடு")
    name = models.CharField(max_length=100, verbose_name="பெயர்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "நிலை"; ordering = ['order']


class AdminProfile(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, verbose_name="இருப்பிடம்")
    address  = models.TextField(verbose_name="முகவரி")
    phone    = models.CharField(max_length=15, verbose_name="தொலைபேசி")
    def __str__(self): return f"{self.user.get_full_name()} - {self.location}"


# ─────────────────────────────────────────────
#  CANDIDATE ABSTRACT BASE
# ─────────────────────────────────────────────

class BaseCandidateModel(models.Model):
    uid                      = models.CharField(max_length=20, unique=True, editable=False)
    name                     = models.CharField(max_length=200, verbose_name="பெயர்")
    date_of_birth            = models.DateField(verbose_name="பிறந்த தேதி")
    rasi                     = models.ForeignKey(Rasi, on_delete=models.SET_NULL, null=True, verbose_name="ராசி")
    nachathiram              = models.ForeignKey(Nachathiram, on_delete=models.SET_NULL, null=True, verbose_name="நட்சத்திரம்")
    profession               = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, verbose_name="தொழில்")
    profession_comments      = models.TextField(blank=True, verbose_name="தொழில் விவரம்")
    educational_qualification= models.CharField(max_length=200, verbose_name="கல்வித் தகுதி")
    annual_income            = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="வருடாந்திர வருமானம்")
    monthly_salary           = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="மாத சம்பளம்")
    height                   = models.CharField(max_length=20, verbose_name="உயரம்")
    caste                    = models.CharField(max_length=100, verbose_name="சாதி")
    sub_caste                = models.CharField(max_length=100, blank=True, verbose_name="உட்சாதி")
    sevadosham               = models.ForeignKey(Sevadosham, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="செவ்வாய் தோஷம்")
    ragu_kethu               = models.CharField(max_length=50, blank=True, verbose_name="ராகு/கேது")
    property_value           = models.CharField(max_length=200, blank=True, verbose_name="சொத்து மதிப்பு")
    jathagam_type            = models.ForeignKey(JathagamType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ஜாதகம் வகை")
    state                    = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, verbose_name="மாநிலம்")
    district                 = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name="மாவட்டம்")
    status                   = models.ForeignKey(CandidateStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="நிலை")
    premium_start_date       = models.DateField(null=True, blank=True, verbose_name="பிரீமியம் தொடக்க தேதி")
    premium_end_date         = models.DateField(null=True, blank=True, verbose_name="பிரீமியம் முடிவு தேதி")
    is_paid                  = models.BooleanField(default=True, verbose_name="கட்டணம் செலுத்தியது")
    created_by               = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_at               = models.DateTimeField(auto_now_add=True)
    updated_at               = models.DateTimeField(auto_now=True)
    is_new                   = models.BooleanField(default=True)

    # ராசி Chart - FK to Planet
    rasi_h1  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 1")
    rasi_h2  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 2")
    rasi_h3  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 3")
    rasi_h4  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 4")
    rasi_h5  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 5")
    rasi_h6  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 6")
    rasi_h7  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 7")
    rasi_h8  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 8")
    rasi_h9  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 9")
    rasi_h10 = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 10")
    rasi_h11 = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 11")
    rasi_h12 = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராசி வீடு 12")

    # நவாம்சம் Chart - FK to Planet
    navamsam_h1  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 1")
    navamsam_h2  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 2")
    navamsam_h3  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 3")
    navamsam_h4  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 4")
    navamsam_h5  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 5")
    navamsam_h6  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 6")
    navamsam_h7  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 7")
    navamsam_h8  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 8")
    navamsam_h9  = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 9")
    navamsam_h10 = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 10")
    navamsam_h11 = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 11")
    navamsam_h12 = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="நவாம்சம் வீடு 12")

    # Family
    father_name       = models.CharField(max_length=200, blank=True, verbose_name="தந்தை பெயர்")
    father_profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="தந்தை தொழில்")
    mother_name       = models.CharField(max_length=200, blank=True, verbose_name="தாய் பெயர்")
    mother_profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="தாய் தொழில்")
    siblings_info     = models.TextField(blank=True, verbose_name="உடன்பிறந்தோர் விவரம்")

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

    class Meta:
        abstract = True
        ordering = ['-created_at']


# ─────────────────────────────────────────────
#  MALE / FEMALE CANDIDATE
# ─────────────────────────────────────────────

class MaleCandidate(BaseCandidateModel):
    @property
    def gender(self): return 'M'

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = f"M{str(uuid.uuid4().int)[:6]}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "ஆண் விண்ணப்பதாரர்"
        ordering = ['-created_at']


class FemaleCandidate(BaseCandidateModel):
    @property
    def gender(self): return 'F'

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = f"F{str(uuid.uuid4().int)[:6]}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "பெண் விண்ணப்பதாரர்"
        ordering = ['-created_at']


# ─────────────────────────────────────────────
#  PHOTO
# ─────────────────────────────────────────────

class CandidatePhoto(models.Model):
    male_candidate   = models.ForeignKey(MaleCandidate,   on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    female_candidate = models.ForeignKey(FemaleCandidate, on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    photo       = models.ImageField(upload_to='photos/')
    is_primary  = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def candidate(self):
        return self.male_candidate or self.female_candidate

    class Meta: verbose_name = "புகைப்படம்"


class ShadowCandidate(models.Model):
    original_data = models.JSONField()
    created_at    = models.DateTimeField(auto_now_add=True)
    notes         = models.TextField(blank=True)
    class Meta: verbose_name = "நிலுவை விண்ணப்பம்"
