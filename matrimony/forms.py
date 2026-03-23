from django import forms
from .models import (MaleCandidate, FemaleCandidate, Rasi, Nachathiram,
                     Profession, JathagamType, Planet, Sevadosham,
                     CandidateStatus, State, District,
                     TamilYear, TamilMonth, TamilKizhamai, TamilDate, OwnHouse, BirthOrder, PremiumType,
                     Complexion, Caste, SubCaste, Height)

COMMON_EXCLUDE = ['uid', 'created_by', 'created_at', 'updated_at', 'is_new']

COMMON_WIDGETS = {
    'name':                      forms.TextInput(attrs={'class': 'form-control'}),
    'rasi':                      forms.Select(attrs={'class': 'form-select', 'id': 'id_rasi'}),
    'lagnam':                    forms.Select(attrs={'class': 'form-select', 'id': 'id_lagnam'}),
    'nachathiram':               forms.Select(attrs={'class': 'form-select', 'id': 'id_nachathiram'}),
    'profession':                forms.Select(attrs={'class': 'form-select'}),
    'profession_comments':       forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
    'educational_qualification': forms.TextInput(attrs={'class': 'form-control'}),
    'annual_income':             forms.NumberInput(attrs={'class': 'form-control'}),
    'monthly_salary':            forms.NumberInput(attrs={'class': 'form-control'}),
    'height':                    forms.TextInput(attrs={'class': 'form-control'}),
    'caste':                     forms.TextInput(attrs={'class': 'form-control'}),
    'sub_caste':                 forms.TextInput(attrs={'class': 'form-control'}),
    'sevadosham':                forms.Select(attrs={'class': 'form-select'}),
    'ragu_kethu':                forms.Select(attrs={'class': 'form-select'}),
    'address_name':              forms.TextInput(attrs={'class': 'form-control', 'id': 'id_address_name'}),
    'old_reg_no':                forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ப.பதிவு எண்'}),
    'address_line1':             forms.TextInput(attrs={'class': 'form-control'}),
    'address_line2':             forms.TextInput(attrs={'class': 'form-control'}),
    'address_line3':             forms.TextInput(attrs={'class': 'form-control'}),
    'pincode':                   forms.TextInput(attrs={'class': 'form-control', 'maxlength': '6', 'pattern': '[0-9]{6}', 'inputmode': 'numeric'}),
    'mobile_number':             forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15', 'inputmode': 'numeric'}),
    'whatsapp_number':           forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15', 'inputmode': 'numeric'}),
    'property_value':            forms.TextInput(attrs={'class': 'form-control'}),
    'state':                     forms.Select(attrs={'class': 'form-select', 'id': 'id_state'}),
    'district':                  forms.Select(attrs={'class': 'form-select', 'id': 'id_district'}),
    'status':                    forms.Select(attrs={'class': 'form-select'}),
    'father_profession':         forms.Select(attrs={'class': 'form-select'}),
    'mother_profession':         forms.Select(attrs={'class': 'form-select'}),
    'tamil_year':                forms.Select(attrs={'class': 'form-select'}),
    'tamil_month':               forms.Select(attrs={'class': 'form-select'}),
    'tamil_kizhamai':            forms.Select(attrs={'class': 'form-select'}),
    'tamil_date':                forms.Select(attrs={'class': 'form-select'}),
    'own_house':                 forms.Select(attrs={'class': 'form-select'}),
    'premium_type':              forms.Select(attrs={'class': 'form-select'}),
    'birth_time':                forms.TimeInput(attrs={'class': 'form-control', 'placeholder': '10:45 AM', 'type': 'time'}),
    'complexion':                forms.Select(attrs={'class': 'form-select'}),
    'height':                    forms.Select(attrs={'class': 'form-select'}),
    'caste':                     forms.Select(attrs={'class': 'form-select', 'id': 'id_caste'}),
    'sub_caste':                 forms.Select(attrs={'class': 'form-select', 'id': 'id_sub_caste'}),
    'birth_order':               forms.Select(attrs={'class': 'form-select'}),
    'thisai_iruppu':             forms.TextInput(attrs={'class': 'form-control', 'style': 'height:38px;'}),
    'birth_place':               forms.TextInput(attrs={'class': 'form-control'}),
    'native_place':              forms.TextInput(attrs={'class': 'form-control'}),
}


class BaseCandidateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'], label="பிறந்த தேதி"
    )
    premium_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False, label="பிரீமியம் தொடக்க தேதி"
    )
    premium_end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False, label="பிரீமியம் முடிவு தேதி"
    )


def _get_active_status():
    from .models import CandidateStatus
    try:
        return CandidateStatus.objects.get(code='searching')
    except Exception:
        try:
            return CandidateStatus.objects.get(code='active')
        except Exception:
            return None



def _get_silver_type():
    from .models import PremiumType
    try:
        return PremiumType.objects.get(code='silver')
    except Exception:
        return None

def _get_default_complexion():
    from .models import Complexion
    try:
        return Complexion.objects.get(name='மாநிறம்')
    except Exception:
        return None

def _get_default_caste():
    from .models import Caste
    try:
        return Caste.objects.get(name='வன்னியர்')
    except Exception:
        return None

class MaleCandidateForm(BaseCandidateForm):
    class Meta:
        model = MaleCandidate
        exclude = COMMON_EXCLUDE
        widgets = COMMON_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get('instance'):
            self.fields['status'].initial = _get_active_status()
            self.fields['premium_type'].initial = _get_silver_type()
            self.fields['complexion'].initial = _get_default_complexion()
            self.fields['caste'].initial = _get_default_caste()
            from datetime import date
            today = date.today()
            self.fields['premium_start_date'].initial = today
            # Add exactly 6 months (same day, 6 months later minus 1 day)
            month = today.month + 6
            year = today.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            import calendar
            day = min(today.day, calendar.monthrange(year, month)[1])
            end_date = date(year, month, day) - __import__('datetime').timedelta(days=1)
            self.fields['premium_end_date'].initial = end_date


class FemaleCandidateForm(BaseCandidateForm):
    class Meta:
        model = FemaleCandidate
        exclude = COMMON_EXCLUDE
        widgets = COMMON_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get('instance'):
            self.fields['status'].initial = _get_active_status()
            self.fields['premium_type'].initial = _get_silver_type()
            self.fields['complexion'].initial = _get_default_complexion()
            self.fields['caste'].initial = _get_default_caste()
            from datetime import date
            today = date.today()
            self.fields['premium_start_date'].initial = today
            # Add exactly 6 months (same day, 6 months later minus 1 day)
            month = today.month + 6
            year = today.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            import calendar
            day = min(today.day, calendar.monthrange(year, month)[1])
            end_date = date(year, month, day) - __import__('datetime').timedelta(days=1)
            self.fields['premium_end_date'].initial = end_date
