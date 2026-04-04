from django.db import models
from django.contrib.auth.models import User
import uuid


# ─────────────────────────────────────────────
#  LOOKUP TABLES  (all editable via admin)
# ─────────────────────────────────────────────

class State(models.Model):
    name  = models.CharField(max_length=100)
    order = models.IntegerField(default=99)
    def __str__(self): return self.name
    class Meta: verbose_name = "மாநிலம்"; ordering = ['order', 'name']

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name  = models.CharField(max_length=100)
    order = models.IntegerField(default=99)
    def __str__(self): return self.name
    class Meta: verbose_name = "மாவட்டம்"; ordering = ['order', 'name']

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



class TamilYear(models.Model):
    name  = models.CharField(max_length=50, verbose_name="தமிழ் வருடம்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "தமிழ் வருடம்"; ordering = ['order']

class TamilMonth(models.Model):
    name  = models.CharField(max_length=50, verbose_name="தமிழ் மாதம்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "தமிழ் மாதம்"; ordering = ['order']

class TamilKizhamai(models.Model):
    name  = models.CharField(max_length=50, verbose_name="தமிழ் கிழமை")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "தமிழ் கிழமை"; ordering = ['order']

class TamilDate(models.Model):
    name  = models.CharField(max_length=10, verbose_name="தமிழ் தேதி")
    order = models.PositiveIntegerField(default=99)
    def __str__(self): return self.name
    class Meta: verbose_name = "தமிழ் தேதி"; ordering = ['order']

class OwnHouse(models.Model):
    code  = models.CharField(max_length=10, unique=True, verbose_name="குறியீடு")
    name  = models.CharField(max_length=50, verbose_name="பெயர்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "சொந்த வீடு"; ordering = ['order']

class RaguKethu(models.Model):
    code  = models.CharField(max_length=10, unique=True, verbose_name="குறியீடு")
    name  = models.CharField(max_length=50, verbose_name="பெயர்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "ராகு/கேது"; ordering = ['order']

class PremiumType(models.Model):
    code          = models.CharField(max_length=20, unique=True, verbose_name="குறியீடு")
    name          = models.CharField(max_length=50, verbose_name="பெயர்")
    order         = models.PositiveIntegerField(default=0)
    weekly_limit  = models.PositiveIntegerField(default=5, verbose_name="வார வரம்பு (0=வரம்பற்றது)")
    def __str__(self): return self.name
    class Meta: verbose_name = "பிரீமியம் வகை"; ordering = ['order']

class BirthOrder(models.Model):
    name  = models.CharField(max_length=10, verbose_name="பிறப்பு வரிசை")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "பிறப்பு வரிசை"; ordering = ['order']

class Complexion(models.Model):
    name  = models.CharField(max_length=50, verbose_name="நிறம்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "நிறம்"; ordering = ['order']

class Caste(models.Model):
    name  = models.CharField(max_length=100, verbose_name="சாதி")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "சாதி"; ordering = ['order']

class SubCaste(models.Model):
    caste = models.ForeignKey(Caste, on_delete=models.CASCADE, related_name='sub_castes', verbose_name="சாதி")
    name  = models.CharField(max_length=100, verbose_name="உட்பிரிவு")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "உட்பிரிவு"; ordering = ['order', 'name']

class Height(models.Model):
    name  = models.CharField(max_length=20, verbose_name="உயரம்")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "உயரம்"; ordering = ['order']


class Relation(models.Model):
    name  = models.CharField(max_length=50, verbose_name="உறவு")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "உறவு"; ordering = ['order']

class MaritalStatus(models.Model):
    name  = models.CharField(max_length=50, verbose_name="திருமண நிலை")
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
    class Meta: verbose_name = "திருமண நிலை"; ordering = ['order']

class AdminProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    location       = models.CharField(max_length=200, verbose_name="இருப்பிடம்")
    address_line1  = models.CharField(max_length=200, blank=True, verbose_name="முகவரி வரி 1")
    address_line2  = models.CharField(max_length=200, blank=True, verbose_name="முகவரி வரி 2")
    address_line3  = models.CharField(max_length=200, blank=True, verbose_name="முகவரி வரி 3")
    phone          = models.CharField(max_length=15, verbose_name="தொலைபேசி")
    alternate_phone= models.CharField(max_length=15, blank=True, verbose_name="மாற்று தொலைபேசி")
    email          = models.EmailField(blank=True, verbose_name="மின்னஞ்சல்")
    def __str__(self): return f"{self.user.get_full_name()} - {self.location}"


# ─────────────────────────────────────────────
#  CANDIDATE ABSTRACT BASE
# ─────────────────────────────────────────────

class BaseCandidateModel(models.Model):
    uid                      = models.CharField(max_length=20, unique=True, editable=False)
    old_reg_no               = models.CharField(max_length=50, blank=True, verbose_name="ப.பதிவு எண்")
    name                     = models.CharField(max_length=200, verbose_name="பெயர்")
    date_of_birth            = models.DateField(verbose_name="பிறந்த தேதி")
    birth_time               = models.TimeField(null=True, blank=True, verbose_name="பிறந்த நேரம்")
    rasi                     = models.ForeignKey(Rasi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ராசி", related_name="+")
    lagnam                   = models.ForeignKey(Rasi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="லக்னம்", related_name="+")
    nachathiram              = models.ForeignKey(Nachathiram, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="நட்சத்திரம்")
    profession               = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="தொழில்")
    profession_comments      = models.TextField(blank=True, verbose_name="தொழில் விவரம்")
    educational_qualification= models.CharField(max_length=200, blank=True, verbose_name="கல்வித் தகுதி")
    annual_income            = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="வருடாந்திர வருமானம்")
    monthly_salary           = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="மாத சம்பளம்")
    height                   = models.ForeignKey('Height', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="உயரம்")
    caste                    = models.ForeignKey('Caste', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="சாதி")
    sub_caste                = models.ForeignKey('SubCaste', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="உட்பிரிவு")
    complexion               = models.ForeignKey('Complexion', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="நிறம்")
    sevadosham               = models.ForeignKey(Sevadosham, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="செவ்வாய் தோஷம்")
    ragu_kethu               = models.ForeignKey('RaguKethu', on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="ராகு/கேது")
    property_value           = models.CharField(max_length=200, blank=True, verbose_name="சொத்து மதிப்பு")
    state                    = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="மாநிலம்")
    district                 = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="மாவட்டம்")
    status                   = models.ForeignKey(CandidateStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="நிலை")
    premium_start_date       = models.DateField(null=True, blank=True, verbose_name="பிரீமியம் தொடக்க தேதி")
    premium_end_date         = models.DateField(null=True, blank=True, verbose_name="பிரீமியம் முடிவு தேதி")
    premium_type             = models.ForeignKey('PremiumType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="பிரீமியம் வகை")
    created_by               = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_at               = models.DateTimeField(auto_now_add=True)
    updated_at               = models.DateTimeField(auto_now=True)
    is_new                   = models.BooleanField(default=True)

    # ஜாதகம் planets are now stored in JathagamEntry (see below)
    # Use candidate.get_jathagam_map() to get {chart_type: {house_number: "சூ, செ"}}

    # Family

    # Tamil calendar & property
    tamil_year  = models.ForeignKey('TamilYear',  on_delete=models.SET_NULL, null=True, blank=True, verbose_name="தமிழ் வருடம்")
    tamil_month = models.ForeignKey('TamilMonth', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="தமிழ் மாதம்")
    tamil_kizhamai = models.ForeignKey('TamilKizhamai', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="தமிழ் கிழமை")
    tamil_date     = models.ForeignKey('TamilDate',     on_delete=models.SET_NULL, null=True, blank=True, verbose_name="தமிழ் தேதி")
    own_house    = models.ForeignKey('OwnHouse',   on_delete=models.SET_NULL, null=True, blank=True, verbose_name="சொந்த வீடு")
    birth_order  = models.ForeignKey('BirthOrder', on_delete=models.SET_NULL, null=True, blank=False, verbose_name="பிறப்பு வரிசை")
    thisai_iruppu= models.CharField(max_length=100, blank=True, verbose_name="திசை இருப்பு")
    birth_place  = models.CharField(max_length=200, blank=True, verbose_name="பிறந்த ஊர்")
    native_place = models.CharField(max_length=200, blank=True, verbose_name="பூர்வீகம்")

    # முகவரி விவரங்கள்
    address_name    = models.CharField(max_length=200, blank=True, verbose_name="பெயர்")
    address_line1   = models.CharField(max_length=200, blank=True, verbose_name="முகவரி வரி 1")
    address_line2   = models.CharField(max_length=200, blank=True, verbose_name="முகவரி வரி 2")
    address_line3   = models.CharField(max_length=200, blank=True, verbose_name="முகவரி வரி 3")
    pincode         = models.CharField(max_length=10, blank=True, verbose_name="பின்கோட்")
    mobile_number   = models.CharField(max_length=15, blank=True, verbose_name="கைபேசி எண்")
    whatsapp_number = models.CharField(max_length=15, blank=True, verbose_name="வாட்ஸ்அப் எண்")

    def get_jathagam_map(self):
        """
        Returns a nested dict for both charts:
        {
          'R': {1: 'சூ, செ', 2: '', 3: 'கு', ...},
          'N': {1: '',        2: 'ல',  3: '', ...},
        }
        All 12 houses are always present (empty string if no planets).
        Used by templates to render the jathagam grid without extra queries
        when called once and passed to context.
        """
        gender = 'M' if isinstance(self, MaleCandidate) else 'F'
        entries = (
            JathagamEntry.objects
            .filter(candidate_gender=gender, candidate_id=self.pk)
            .select_related('planet')
            .order_by('chart_type', 'house_number', 'order')
        )
        result = {
            'R': {h: [] for h in range(1, 13)},
            'N': {h: [] for h in range(1, 13)},
        }
        for e in entries:
            result[e.chart_type][e.house_number].append(e.planet.code)
        # Convert lists to comma-separated strings
        return {
            ct: {h: ', '.join(planets) for h, planets in houses.items()}
            for ct, houses in result.items()
        }

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
            status_code = self.status.code if self.status else ''
            prefix = 'MM' if status_code == 'remarriage' else 'M'
            count = MaleCandidate.objects.count() + 1
            uid = f"{prefix}{count:07d}"
            while MaleCandidate.objects.filter(uid=uid).exists():
                count += 1
                uid = f"{prefix}{count:07d}"
            self.uid = uid
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "ஆண் விண்ணப்பதாரர்"
        ordering = ['-created_at']


class FemaleCandidate(BaseCandidateModel):
    @property
    def gender(self): return 'F'

    def save(self, *args, **kwargs):
        if not self.uid:
            status_code = self.status.code if self.status else ''
            prefix = 'MF' if status_code == 'remarriage' else 'F'
            count = FemaleCandidate.objects.count() + 1
            uid = f"{prefix}{count:07d}"
            while FemaleCandidate.objects.filter(uid=uid).exists():
                count += 1
                uid = f"{prefix}{count:07d}"
            self.uid = uid
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "பெண் விண்ணப்பதாரர்"
        ordering = ['-created_at']


# ─────────────────────────────────────────────
#  PHOTO
# ─────────────────────────────────────────────

def candidate_photo_upload(instance, filename):
    import os
    candidate = instance.male_candidate or instance.female_candidate
    uid = candidate.uid if candidate else 'unknown'
    return f'photos/{uid}.jpg'


class CandidatePhoto(models.Model):
    male_candidate   = models.ForeignKey(MaleCandidate,   on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    female_candidate = models.ForeignKey(FemaleCandidate, on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    photo       = models.ImageField(upload_to=candidate_photo_upload)
    is_primary  = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def candidate(self):
        return self.male_candidate or self.female_candidate

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Compress photo after saving
        if self.photo:
            try:
                from PIL import Image
                import os
                path = self.photo.path
                img = Image.open(path)
                # Convert to RGB (handles PNG with transparency)
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')
                # Resize if larger than 800px on any side
                max_size = 800
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.LANCZOS)
                # Save as JPEG with 85% quality (good balance)
                img.save(path, 'JPEG', quality=85, optimize=True)
            except Exception:
                pass

    class Meta: verbose_name = "புகைப்படம்"


from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=CandidatePhoto)
def delete_photo_file(sender, instance, **kwargs):
    """Auto-delete photo file from disk when CandidatePhoto record is deleted"""
    import os
    if instance.photo and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)


class FamilyMember(models.Model):
    GENDER_CHOICES = [('M', 'ஆண்'), ('F', 'பெண்')]
    candidate_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    candidate_id     = models.PositiveIntegerField()
    name             = models.CharField(max_length=200, verbose_name="பெயர்")
    education        = models.CharField(max_length=200, blank=True, verbose_name="படிப்பு")
    relation         = models.ForeignKey(Relation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="உறவு")
    marital_status   = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="திருமணம்")
    job_info         = models.CharField(max_length=200, blank=True, verbose_name="பணி விவரம்")
    order            = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "குடும்பத்தினர்"

    def __str__(self):
        return f"{self.name} ({self.relation})"

class JathagamEntry(models.Model):
    """
    Stores planets placed in each house of the jathagam chart.
    Replaces the 24 single-planet FK columns that were on the candidate models.

    One row = one planet in one house of one chart for one candidate.
    A house with சூ, செ, கு has 3 rows (order=1,2,3).

    chart_type: 'R' = ராசி, 'N' = நவாம்சம்
    house_number: 1–12
    order: display order of the planet within the house (1 = first shown)
    """
    CHART_CHOICES = [('R', 'ராசி'), ('N', 'நவாம்சம்')]
    GENDER_CHOICES = [('M', 'ஆண்'), ('F', 'பெண்')]

    candidate_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='பாலினம்')
    candidate_id     = models.PositiveIntegerField(verbose_name='விண்ணப்பதாரர் ID')
    chart_type       = models.CharField(max_length=1, choices=CHART_CHOICES, verbose_name='சார்ட் வகை')
    house_number     = models.PositiveSmallIntegerField(verbose_name='வீடு எண்')
    planet           = models.ForeignKey(Planet, on_delete=models.CASCADE, verbose_name='கோள்')
    order            = models.PositiveSmallIntegerField(default=1, verbose_name='வரிசை')

    class Meta:
        verbose_name = 'ஜாதகம் பதிவு'
        ordering = ['chart_type', 'house_number', 'order']
        indexes = [
            models.Index(fields=['candidate_gender', 'candidate_id'], name='jathagam_candidate_idx'),
            models.Index(fields=['candidate_gender', 'candidate_id', 'chart_type'], name='jathagam_candidate_chart_idx'),
        ]

    def __str__(self):
        return f"{self.candidate_gender}{self.candidate_id} | {self.chart_type} H{self.house_number} | {self.planet.code}"


# ─────────────────────────────────────────────
#  CANDIDATE EXPECTATION
# ─────────────────────────────────────────────

class CandidateExpectation(models.Model):
    GENDER_CHOICES  = [('M', 'ஆண்'), ('F', 'பெண்')]
    JOB_TYPE_CHOICES = [
        ('any',      'எதுவும்'),
        ('govt',     'அரசு'),
        ('private',  'தனியார்'),
        ('business', 'வியாபாரம்'),
    ]
    candidate_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="பாலினம்")
    candidate_id     = models.PositiveIntegerField(verbose_name="விண்ணப்பதாரர் ID")
    salary_min       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="குறைந்த சம்பளம்")
    sevadosham_ok    = models.ForeignKey('Sevadosham', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="செவ்வாய் தோஷம்")
    own_house_pref   = models.ForeignKey('OwnHouse', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="சொந்த வீடு")
    marital_status_ok= models.ForeignKey('MaritalStatus', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="திருமண நிலை")
    education_min    = models.CharField(max_length=200, blank=True, verbose_name="கல்வித் தகுதி")
    job_type         = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='any', verbose_name="வேலை வகை")
    notes            = models.TextField(blank=True, verbose_name="குறிப்புகள்")
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "எதிர்பார்ப்பு"
        unique_together = [('candidate_gender', 'candidate_id')]

    def __str__(self):
        return f"{self.candidate_gender}{self.candidate_id} எதிர்பார்ப்பு"


class ExpectationNachathiram(models.Model):
    expectation  = models.ForeignKey(CandidateExpectation, on_delete=models.CASCADE, related_name='nachathirams')
    nachathiram  = models.ForeignKey(Nachathiram, on_delete=models.CASCADE, verbose_name="நட்சத்திரம்")
    class Meta: unique_together = [('expectation', 'nachathiram')]


class ExpectationSubCaste(models.Model):
    expectation = models.ForeignKey(CandidateExpectation, on_delete=models.CASCADE, related_name='sub_castes')
    sub_caste   = models.ForeignKey(SubCaste, on_delete=models.CASCADE, verbose_name="உட்பிரிவு")
    class Meta: unique_together = [('expectation', 'sub_caste')]


class ExpectationDistrict(models.Model):
    expectation = models.ForeignKey(CandidateExpectation, on_delete=models.CASCADE, related_name='districts')
    district    = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="மாவட்டம்")
    class Meta: unique_together = [('expectation', 'district')]


class ExpectationProfession(models.Model):
    expectation = models.ForeignKey(CandidateExpectation, on_delete=models.CASCADE, related_name='professions')
    profession  = models.ForeignKey(Profession, on_delete=models.CASCADE, verbose_name="தொழில்")
    class Meta: unique_together = [('expectation', 'profession')]


class ExpectationComplexion(models.Model):
    expectation = models.ForeignKey(CandidateExpectation, on_delete=models.CASCADE, related_name='complexions')
    complexion  = models.ForeignKey(Complexion, on_delete=models.CASCADE, verbose_name="நிறம்")
    class Meta: unique_together = [('expectation', 'complexion')]


# ─────────────────────────────────────────────
#  BIO TOKEN  (secure shareable bio links)
# ─────────────────────────────────────────────

class BioToken(models.Model):
    GENDER_CHOICES = [('M', 'ஆண்'), ('F', 'பெண்')]
    token            = models.CharField(max_length=64, unique=True, verbose_name="டோக்கன்")
    candidate_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    candidate_id     = models.PositiveIntegerField()
    created_at       = models.DateTimeField(auto_now_add=True)
    expires_at       = models.DateTimeField(verbose_name="காலாவதி தேதி")

    class Meta:
        verbose_name = "பயோ டோக்கன்"
        indexes = [models.Index(fields=['token'], name='bio_token_idx')]

    def __str__(self):
        return f"{self.candidate_gender}{self.candidate_id} - {self.token[:8]}..."

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    @classmethod
    def create_for_candidate(cls, gender, candidate_id):
        import secrets
        from django.utils import timezone
        from datetime import timedelta
        # Never delete old tokens — BioSendLog FKs depend on them
        # Just create a new token each time
        return cls.objects.create(
            token=secrets.token_urlsafe(32),
            candidate_gender=gender,
            candidate_id=candidate_id,
            expires_at=timezone.now() + timedelta(days=WeeklyBioConfig.get().bio_token_expiry_days),
        )


# ─────────────────────────────────────────────
#  BIO SEND LOG
# ─────────────────────────────────────────────

class BioSendLog(models.Model):
    GENDER_CHOICES = [('M', 'ஆண்'), ('F', 'பெண்')]
    STATUS_CHOICES = [('pending', 'நிலுவை'), ('sent', 'அனுப்பியது'), ('failed', 'தோல்வி')]

    sender_gender   = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="அனுப்புபவர் பாலினம்")
    sender_id       = models.PositiveIntegerField(verbose_name="அனுப்புபவர் ID")
    receiver_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="பெறுபவர் பாலினம்")
    receiver_id     = models.PositiveIntegerField(verbose_name="பெறுபவர் ID")
    bio_token       = models.ForeignKey(BioToken, null=True, blank=True, on_delete=models.SET_NULL)
    month_year      = models.CharField(max_length=10, verbose_name="வார தொடக்கம்")  # e.g. 2026-03-22
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    prepared_at     = models.DateTimeField(auto_now_add=True, verbose_name="தயாரித்த நேரம்")
    sent_at         = models.DateTimeField(null=True, blank=True, verbose_name="அனுப்பிய நேரம்")

    class Meta:
        verbose_name = "அனுப்பல் பதிவு"
        ordering = ['-prepared_at']
        indexes = [
            models.Index(fields=['sender_gender', 'sender_id', 'month_year'], name='biosend_sender_idx'),
            models.Index(fields=['sender_gender', 'sender_id', 'receiver_gender', 'receiver_id'], name='biosend_pair_idx'),
        ]

    def __str__(self):
        return f"{self.sender_gender}{self.sender_id} → {self.receiver_gender}{self.receiver_id} ({self.month_year})"


# ─────────────────────────────────────────────
#  WEEKLY BIO RUN LOG
# ─────────────────────────────────────────────

class WeeklyBioRun(models.Model):
    run_at           = models.DateTimeField(auto_now_add=True, verbose_name="இயக்கிய நேரம்")
    run_by           = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="இயக்கியவர்")
    week_start       = models.DateField(verbose_name="வார தொடக்கம் (ஞாயிறு)")
    week_end         = models.DateField(verbose_name="வார முடிவு (சனி)")
    male_processed   = models.PositiveIntegerField(default=0, verbose_name="ஆண் விண்ணப்பதாரர்கள்")
    female_processed = models.PositiveIntegerField(default=0, verbose_name="பெண் விண்ணப்பதாரர்கள்")
    matches_created  = models.PositiveIntegerField(default=0, verbose_name="பொருத்தங்கள் உருவாக்கப்பட்டன")
    notes            = models.TextField(blank=True, verbose_name="குறிப்புகள்")

    class Meta:
        verbose_name = "வார இயக்க பதிவு"
        ordering = ['-run_at']

    def __str__(self):
        return f"வார இயக்கம் {self.week_start} — {self.matches_created} பொருத்தங்கள்"


# ─────────────────────────────────────────────
#  MARRIED CANDIDATE
# ─────────────────────────────────────────────

class MarriedCandidate(models.Model):
    GENDER_CHOICES = [('M', 'ஆண்'), ('F', 'பெண்')]
    gender          = models.CharField(max_length=1, choices=GENDER_CHOICES)
    candidate_id    = models.PositiveIntegerField()
    uid             = models.CharField(max_length=20)
    name            = models.CharField(max_length=200)
    married_at      = models.DateTimeField(auto_now_add=True, verbose_name="திருமணம் பதிவு நேரம்")
    date_of_birth   = models.DateField(null=True, blank=True)
    mobile_number   = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    district        = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    created_by      = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "திருமணமான வரன்"
        ordering = ['-married_at']
        unique_together = [['gender', 'candidate_id']]

    def __str__(self):
        return f"{self.uid} — {self.name}"


# ─────────────────────────────────────────────
#  SIGNAL: Move to MarriedCandidate when status = married
# ─────────────────────────────────────────────

from django.db.models.signals import pre_save
from django.dispatch import receiver

def _snapshot_to_married(candidate, gender):
    """Copy candidate data to MarriedCandidate table."""
    MarriedCandidate.objects.update_or_create(
        gender=gender,
        candidate_id=candidate.pk,
        defaults={
            'uid': candidate.uid,
            'name': candidate.name,
            'date_of_birth': candidate.date_of_birth,
            'mobile_number': candidate.mobile_number or '',
            'whatsapp_number': candidate.whatsapp_number or '',
            'district': candidate.district,
            'created_by': candidate.created_by,
        }
    )

def _assign_remarriage_uid(instance, prefix):
    """Assign MM/MF prefixed UID when status changes to remarriage."""
    new_uid = f"{prefix}{instance.pk:07d}"
    # Ensure uniqueness
    if prefix == 'MM':
        while MaleCandidate.objects.filter(uid=new_uid).exclude(pk=instance.pk).exists():
            new_uid = f"{prefix}{int(new_uid[2:])+1:07d}"
    else:
        while FemaleCandidate.objects.filter(uid=new_uid).exclude(pk=instance.pk).exists():
            new_uid = f"{prefix}{int(new_uid[2:])+1:07d}"
    instance.uid = new_uid


@receiver(pre_save, sender=MaleCandidate)
def male_candidate_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = MaleCandidate.objects.get(pk=instance.pk)
        old_code = old.status.code if old.status else ''
        new_code = instance.status.code if instance.status else ''
        # Status → married: snapshot
        if new_code == 'married' and old_code != 'married':
            _snapshot_to_married(instance, 'M')
        elif old_code == 'married' and new_code != 'married':
            MarriedCandidate.objects.filter(gender='M', candidate_id=instance.pk).delete()
        # Status → remarriage: reassign UID to MM prefix
        if new_code == 'remarriage' and old_code != 'remarriage':
            if not instance.uid.startswith('MM'):
                _assign_remarriage_uid(instance, 'MM')
        # Status changed away from remarriage: restore M prefix
        elif old_code == 'remarriage' and new_code != 'remarriage' and new_code != 'married':
            if instance.uid.startswith('MM'):
                count = MaleCandidate.objects.count() + 1
                new_uid = f"M{count:07d}"
                while MaleCandidate.objects.filter(uid=new_uid).exclude(pk=instance.pk).exists():
                    count += 1
                    new_uid = f"M{count:07d}"
                instance.uid = new_uid
    except Exception:
        pass


@receiver(pre_save, sender=FemaleCandidate)
def female_candidate_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = FemaleCandidate.objects.get(pk=instance.pk)
        old_code = old.status.code if old.status else ''
        new_code = instance.status.code if instance.status else ''
        # Status → married: snapshot
        if new_code == 'married' and old_code != 'married':
            _snapshot_to_married(instance, 'F')
        elif old_code == 'married' and new_code != 'married':
            MarriedCandidate.objects.filter(gender='F', candidate_id=instance.pk).delete()
        # Status → remarriage: reassign UID to MF prefix
        if new_code == 'remarriage' and old_code != 'remarriage':
            if not instance.uid.startswith('MF'):
                _assign_remarriage_uid(instance, 'MF')
        # Status changed away from remarriage: restore F prefix
        elif old_code == 'remarriage' and new_code != 'remarriage' and new_code != 'married':
            if instance.uid.startswith('MF'):
                count = FemaleCandidate.objects.count() + 1
                new_uid = f"F{count:07d}"
                while FemaleCandidate.objects.filter(uid=new_uid).exclude(pk=instance.pk).exists():
                    count += 1
                    new_uid = f"F{count:07d}"
                instance.uid = new_uid
    except Exception:
        pass


# ─────────────────────────────────────────────
#  WEEKLY BIO CONFIG (admin-editable settings)
# ─────────────────────────────────────────────

class WeeklyBioConfig(models.Model):
    """Singleton config table — always only one row (pk=1)."""

    # Bio token expiry
    bio_token_expiry_days       = models.PositiveIntegerField(default=30, verbose_name="பயோ இணைப்பு காலம் (நாட்கள்)")

    # Married candidate cleanup
    married_cleanup_days        = models.PositiveIntegerField(default=90,  verbose_name="திருமணமான வரன் தக்க வைப்பு (நாட்கள்)")

    # BioSendLog retention
    bio_log_retention_days      = models.PositiveIntegerField(default=365, verbose_name="அனுப்பல் பதிவு தக்க வைப்பு (நாட்கள்)")

    # Default weekly limit (when no premium type assigned)
    default_weekly_limit        = models.PositiveIntegerField(default=5,   verbose_name="இயல்புநிலை வார வரம்பு")

    # Remarriage weekly limits (separate from normal)
    remarriage_silver_limit     = models.PositiveIntegerField(default=5,   verbose_name="மறுமணம் Silver வார வரம்பு")
    remarriage_gold_limit       = models.PositiveIntegerField(default=10,  verbose_name="மறுமணம் Gold வார வரம்பு")
    remarriage_platinum_limit   = models.PositiveIntegerField(default=20,  verbose_name="மறுமணம் Platinum வார வரம்பு")
    remarriage_diamond_limit    = models.PositiveIntegerField(default=0,   verbose_name="மறுமணம் Diamond வார வரம்பு (0=வரம்பற்றது)")

    # Matching rules
    match_age_strict            = models.BooleanField(default=True,  verbose_name="வயது பொருத்தம் கட்டாயம்")
    match_divorced_only         = models.BooleanField(default=True,  verbose_name="மறுமணம் ↔ மறுமணம் மட்டும்")
    max_receivers_per_run       = models.PositiveIntegerField(default=50,  verbose_name="ஒரு இயக்கத்தில் அதிகபட்ச பெறுபவர்கள்")

    # Last updated
    updated_at  = models.DateTimeField(auto_now=True)
    updated_by  = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "வார அனுப்பல் அமைப்பு"

    def __str__(self):
        return "வார அனுப்பல் அமைப்பு"

    @classmethod
    def get(cls):
        """Always returns the singleton config, creating it if missing."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ─────────────────────────────────────────────
#  AUDIT LOG
# ─────────────────────────────────────────────

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'சேர்க்கப்பட்டது'),
        ('update', 'திருத்தப்பட்டது'),
        ('delete', 'நீக்கப்பட்டது'),
        ('status', 'நிலை மாற்றம்'),
        ('premium', 'பிரீமியம் மாற்றம்'),
    ]
    action       = models.CharField(max_length=10, choices=ACTION_CHOICES)
    gender       = models.CharField(max_length=1)
    candidate_id = models.PositiveIntegerField()
    candidate_uid= models.CharField(max_length=20, blank=True)
    candidate_name=models.CharField(max_length=200, blank=True)
    details      = models.TextField(blank=True)
    performed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    performed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "தணிக்கை பதிவு"
        ordering = ['-performed_at']
        indexes = [
            models.Index(fields=['gender', 'candidate_id'], name='audit_candidate_idx'),
            models.Index(fields=['performed_at'], name='audit_time_idx'),
        ]

    def __str__(self):
        return f"{self.get_action_display()} — {self.candidate_uid} ({self.performed_at:%d/%m/%Y %H:%M})"


def _audit(action, candidate, gender, user=None, details=''):
    """Helper to create audit log entry."""
    try:
        AuditLog.objects.create(
            action=action,
            gender=gender,
            candidate_id=candidate.pk,
            candidate_uid=getattr(candidate, 'uid', ''),
            candidate_name=getattr(candidate, 'name', ''),
            details=details,
            performed_by=user,
        )
    except Exception:
        pass  # Never let audit failure break the main operation
