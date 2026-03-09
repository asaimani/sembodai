from django import forms
from .models import (MaleCandidate, FemaleCandidate, Rasi, Nachathiram,
                     Profession, JathagamType, Planet, Sevadosham,
                     CandidateStatus, State, District,
                     TamilYear, TamilMonth, TamilDay, OwnHouse, BirthOrder,
                     Complexion, Caste, SubCaste, Height)

COMMON_EXCLUDE = ['uid', 'created_by', 'created_at', 'updated_at', 'is_new', 'is_paid',
                  'rasi_h1','rasi_h2','rasi_h3','rasi_h4','rasi_h5','rasi_h6',
                  'rasi_h7','rasi_h8','rasi_h9','rasi_h10','rasi_h11','rasi_h12',
                  'navamsam_h1','navamsam_h2','navamsam_h3','navamsam_h4','navamsam_h5','navamsam_h6',
                  'navamsam_h7','navamsam_h8','navamsam_h9','navamsam_h10','navamsam_h11','navamsam_h12']

COMMON_WIDGETS = {
    'name':                      forms.TextInput(attrs={'class': 'form-control'}),
    'rasi':                      forms.Select(attrs={'class': 'form-select', 'id': 'id_rasi'}),
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
    'ragu_kethu':                forms.TextInput(attrs={'class': 'form-control'}),
    'property_value':            forms.TextInput(attrs={'class': 'form-control'}),
    'jathagam_type':             forms.Select(attrs={'class': 'form-select'}),
    'state':                     forms.Select(attrs={'class': 'form-select', 'id': 'id_state'}),
    'district':                  forms.Select(attrs={'class': 'form-select', 'id': 'id_district'}),
    'status':                    forms.Select(attrs={'class': 'form-select'}),
    'father_name':               forms.TextInput(attrs={'class': 'form-control'}),
    'father_profession':         forms.Select(attrs={'class': 'form-select'}),
    'mother_name':               forms.TextInput(attrs={'class': 'form-control'}),
    'mother_profession':         forms.Select(attrs={'class': 'form-select'}),
    'siblings_info':             forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    'tamil_year':                forms.Select(attrs={'class': 'form-select'}),
    'tamil_month':               forms.Select(attrs={'class': 'form-select'}),
    'tamil_day':                 forms.Select(attrs={'class': 'form-select'}),
    'own_house':                 forms.Select(attrs={'class': 'form-select'}),
    'birth_time':                forms.TimeInput(attrs={'class': 'form-control', 'placeholder': '10:45 AM', 'type': 'time'}),
    'complexion':                forms.Select(attrs={'class': 'form-select'}),
    'height':                    forms.Select(attrs={'class': 'form-select'}),
    'caste':                     forms.Select(attrs={'class': 'form-select', 'id': 'id_caste'}),
    'sub_caste':                 forms.Select(attrs={'class': 'form-select', 'id': 'id_sub_caste'}),
    'birth_order':               forms.Select(attrs={'class': 'form-select'}),
    'thisai_iruppu':             forms.TextInput(attrs={'class': 'form-control'}),
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
        return CandidateStatus.objects.get(code='active')
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


class FemaleCandidateForm(BaseCandidateForm):
    class Meta:
        model = FemaleCandidate
        exclude = COMMON_EXCLUDE
        widgets = COMMON_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get('instance'):
            self.fields['status'].initial = _get_active_status()
