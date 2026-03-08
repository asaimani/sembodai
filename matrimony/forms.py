from django import forms
from .models import Candidate, Rasi, Nachathiram, Profession, Jathagam, State, District, PLANET_CHOICES


def planet_select(house_num):
    return forms.ChoiceField(
        choices=PLANET_CHOICES,
        required=False,
        label=f"வீடு {house_num}",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm jathagam-select'})
    )


class CandidateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        label="பிறந்த தேதி"
    )
    premium_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False, label="பிரீமியம் தொடக்க தேதி"
    )
    premium_end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False, label="பிரீமியம் முடிவு தேதி"
    )

    jathagam_h1  = planet_select(1)
    jathagam_h2  = planet_select(2)
    jathagam_h3  = planet_select(3)
    jathagam_h4  = planet_select(4)
    jathagam_h5  = planet_select(5)
    jathagam_h6  = planet_select(6)
    jathagam_h7  = planet_select(7)
    jathagam_h8  = planet_select(8)
    jathagam_h9  = planet_select(9)
    jathagam_h10 = planet_select(10)
    jathagam_h11 = planet_select(11)
    jathagam_h12 = planet_select(12)

    class Meta:
        model = Candidate
        exclude = ['uid', 'created_by', 'created_at', 'updated_at', 'is_new', 'is_paid']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'பெயர் உள்ளிடவும்'}),
            'rasi': forms.Select(attrs={'class': 'form-select', 'id': 'id_rasi'}),
            'nachathiram': forms.Select(attrs={'class': 'form-select', 'id': 'id_nachathiram'}),
            'profession': forms.Select(attrs={'class': 'form-select'}),
            'profession_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'educational_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "எ.கா: 5'8\""}),
            'caste': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_caste': forms.TextInput(attrs={'class': 'form-control'}),
            'sevadosham': forms.Select(attrs={'class': 'form-select'}),
            'ragu_kethu': forms.TextInput(attrs={'class': 'form-control'}),
            'property_value': forms.TextInput(attrs={'class': 'form-control'}),
            'jathagam': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select', 'id': 'id_state'}),
            'district': forms.Select(attrs={'class': 'form-select', 'id': 'id_district'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_profession': forms.Select(attrs={'class': 'form-select'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_profession': forms.Select(attrs={'class': 'form-select'}),
            'siblings_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
