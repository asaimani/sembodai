from django.core.management.base import BaseCommand
from matrimony.models import (Rasi, Nachathiram, Profession, JathagamType,
                               Planet, Sevadosham, CandidateStatus, State, District,
                               TamilYear, TamilMonth, TamilDay, OwnHouse, BirthOrder,
                               Complexion, Caste, SubCaste, Height)

class Command(BaseCommand):
    help = 'Load initial lookup data'

    def handle(self, *args, **kwargs):

        # ── Rasi & Nachathiram ──
        rasis_data = [
            ('மேஷம்',      ['அஸ்வினி', 'பரணி', 'கார்த்திகை 1']),
            ('ரிஷபம்',     ['கார்த்திகை 2,3,4', 'ரோகிணி', 'மிருகசீரிடம் 1,2']),
            ('மிதுனம்',    ['மிருகசீரிடம் 3,4', 'திருவாதிரை', 'புனர்பூசம் 1,2,3']),
            ('கடகம்',      ['புனர்பூசம் 4', 'பூசம்', 'ஆயில்யம்']),
            ('சிம்மம்',    ['மகம்', 'பூரம்', 'உத்திரம் 1']),
            ('கன்னி',      ['உத்திரம் 2,3,4', 'அஸ்தம்', 'சித்திரை 1,2']),
            ('துலாம்',     ['சித்திரை 3,4', 'சுவாதி', 'விசாகம் 1,2,3']),
            ('விருச்சிகம்',['விசாகம் 4', 'அனுஷம்', 'கேட்டை']),
            ('தனுசு',      ['மூலம்', 'பூராடம்', 'உத்திராடம் 1']),
            ('மகரம்',      ['உத்திராடம் 2,3,4', 'திருவோணம்', 'அவிட்டம் 1,2']),
            ('கும்பம்',    ['அவிட்டம் 3,4', 'சதயம்', 'பூரட்டாதி 1,2,3']),
            ('மீனம்',      ['பூரட்டாதி 4', 'உத்திரட்டாதி', 'ரேவதி']),
        ]
        for rasi_name, nachs in rasis_data:
            rasi, _ = Rasi.objects.get_or_create(name=rasi_name)
            for n in nachs:
                Nachathiram.objects.get_or_create(name=n, defaults={'rasi': rasi})

        # ── Professions ──
        for p in ['விவசாயம்','அரசு ஊழியர்','தனியார் நிறுவனம்','வியாபாரம்',
                  'மருத்துவர்','பொறியாளர்','ஆசிரியர்','வழக்கறிஞர்',
                  'கணக்காளர்','காவல்துறை','இராணுவம்','கட்டுமான தொழில்',
                  'வாகன தொழில்','நெசவு தொழில்','IT துறை','வங்கி துறை',
                  'செவிலியர்','சமையல்காரர்','நேசவு தொழில்','பட்டதாரி வேலை இல்லாதவர்']:
            Profession.objects.get_or_create(name=p)

        # ── Jathagam Types ──
        for j in ['ஜாதகம் உள்ளது','ஜாதகம் இல்லை','கணினி ஜாதகம்',
                  'கைப்படி ஜாதகம்','சுவடி ஜாதகம்','நாடி ஜாதகம்']:
            JathagamType.objects.get_or_create(name=j)

        # ── Planets ──
        planets = [
            (1,  'சூ',   'சூரியன் (சூ)'),
            (2,  'ச',    'சந்திரன் (ச)'),
            (3,  'செ',   'செவ்வாய் (செ)'),
            (4,  'பு',   'புதன் (பு)'),
            (5,  'கு',   'குரு (கு)'),
            (6,  'சுக்', 'சுக்கிரன் (சுக்)'),
            (7,  'சனி',  'சனி'),
            (8,  'ரா',   'ராகு (ரா)'),
            (9,  'கே',   'கேது (கே)'),
            (10, 'லக்',  'லக்னம் (லக்)'),
            (11, 'சூ,ச',   'சூரியன் + சந்திரன்'),
            (12, 'சூ,செ',  'சூரியன் + செவ்வாய்'),
            (13, 'சூ,பு',  'சூரியன் + புதன்'),
            (14, 'சூ,கு',  'சூரியன் + குரு'),
            (15, 'சூ,சனி', 'சூரியன் + சனி'),
            (16, 'ச,செ',   'சந்திரன் + செவ்வாய்'),
            (17, 'ச,கு',   'சந்திரன் + குரு'),
            (18, 'ச,சனி',  'சந்திரன் + சனி'),
            (19, 'செ,கு',  'செவ்வாய் + குரு'),
            (20, 'செ,சனி', 'செவ்வாய் + சனி'),
            (21, 'பு,சுக்','புதன் + சுக்கிரன்'),
            (22, 'கு,சனி', 'குரு + சனி'),
            (23, 'ரா,கே',  'ராகு + கேது'),
            (24, 'லக்,சூ', 'லக்னம் + சூரியன்'),
            (25, 'லக்,ச',  'லக்னம் + சந்திரன்'),
            (26, 'லக்,செ', 'லக்னம் + செவ்வாய்'),
            (27, 'லக்,பு', 'லக்னம் + புதன்'),
            (28, 'லக்,கு', 'லக்னம் + குரு'),
            (29, 'லக்,சுக்','லக்னம் + சுக்கிரன்'),
            (30, 'லக்,சனி','லக்னம் + சனி'),
        ]
        for order, code, name in planets:
            Planet.objects.get_or_create(code=code, defaults={'name': name, 'order': order})

        # ── Sevadosham ──
        for order, code, name in [
            (1, 'yes',     'உண்டு'),
            (2, 'no',      'இல்லை'),
            (3, 'partial', 'பாதி'),
        ]:
            Sevadosham.objects.get_or_create(code=code, defaults={'name': name, 'order': order})

        # ── Candidate Status ──
        for order, code, name in [
            (1, 'active',   'செயலில்'),
            (2, 'inactive', 'செயலற்று'),
        ]:
            CandidateStatus.objects.get_or_create(code=code, defaults={'name': name, 'order': order})

        # ── States & Districts (Tamil Nadu + key states) ──
        states_data = {
            'தமிழ்நாடு': [
                'சென்னை','கோயம்புத்தூர்','மதுரை','திருச்சிராப்பள்ளி','சேலம்',
                'திருநெல்வேலி','திண்டுக்கல்','வேலூர்','ஈரோடு','தூத்துக்குடி',
                'கன்னியாகுமரி','விழுப்புரம்','விருதுநகர்','நாமக்கல்','கரூர்',
                'நீலகிரி','திருவாரூர்','நாகப்பட்டினம்','அரியலூர்','பெரம்பலூர்',
                'புதுக்கோட்டை','ரామநாதபுரம்','சிவகங்கை','தேனி','திருப்பூர்',
                'திருவள்ளூர்','கடலூர்','கள்ளக்குறிச்சி','தர்மபுரி','கிருஷ்ணகிரி',
                'மயிலாடுதுறை','தஞ்சாவூர்','திருவண்ணாமலை','விழுப்புரம்',
            ],
            'கேரளா':    ['திருவனந்தபுரம்','கொச்சி','கோழிக்கோடு','த்രிசூர்'],
            'கர்நாடகா': ['பெங்களூரு','மைசூரு','மங்களூரு','ஹுப்பள்ளி'],
            'ஆந்திரப்பிரதேசம்': ['விஜயவாடா','விசாகப்பட்டணம்','திருப்பதி'],
            'தெலங்கானா': ['ஹைதராபாத்','வாரங்கல்'],
            'மகாராஷ்ட்ரா': ['மும்பை','புனே','நாக்பூர்'],
            'தில்லி': ['புது தில்லி'],
            'மேற்கு வங்காளம்': ['கொல்கத்தா'],
            'குஜராத்': ['அகமதாபாத்','சூரத்'],
            'ராஜஸ்தான்': ['ஜெய்ப்பூர்'],
        }
        for state_name, districts in states_data.items():
            state, _ = State.objects.get_or_create(name=state_name)
            for d in districts:
                District.objects.get_or_create(name=d, defaults={'state': state})


        # ── Tamil Years (60 year cycle) ──
        tamil_years = [
            'பிரபவ','விபவ','சுக்ல','பிரமோதூத','பிரஜோத்பத்தி','ஆங்கீரஸ','ஸ்ரீமுக','பவ',
            'யுவ','தாது','ஈஸ்வர','வெகுதான்ய','பிரமாதி','விக்கிரம','விஷு','சித்திரபானு',
            'சுபானு','தாரண','பார்த்திப','வியய','சர்வஜித்','சர்வதாரி','விரோதி','விக்ருதி',
            'கர','நந்தன','விஜய','ஜய','மன்மத','துர்முகி','ஹேவிளம்பி','விளம்பி',
            'விகாரி','சார்வரி','பிலவ','சுபகிருது','சோபகிருது','குரோதி','விஸ்வாவசு','பராபவ',
            'பிலவங்க','கீலக','சௌம்ய','சாதாரண','விரோதகிருது','பரிதாபி','பிரமாதீச','ஆனந்த',
            'ராட்சஸ','நள','பிங்கள','காளயுக்தி','சித்தார்த்தி','ரௌத்திரி','துர்மதி','துந்துபி',
            'ருத்ரோத்காரி','ரக்தாட்சி','குரோதன','அட்சய'
        ]
        for i, y in enumerate(tamil_years, 1):
            TamilYear.objects.get_or_create(name=y, defaults={'order': i})

        # ── Tamil Months ──
        tamil_months = [
            'சித்திரை','வைகாசி','ஆனி','ஆடி','ஆவணி','புரட்டாசி',
            'ஐப்பசி','கார்த்திகை','மார்கழி','தை','மாசி','பங்குனி'
        ]
        for i, m in enumerate(tamil_months, 1):
            TamilMonth.objects.get_or_create(name=m, defaults={'order': i})

        # ── Tamil Days (days of week) ──
        tamil_days = [
            (1, 'ஞாயிற்றுக்கிழமை'),
            (2, 'திங்கட்கிழமை'),
            (3, 'செவ்வாய்க்கிழமை'),
            (4, 'புதன்கிழமை'),
            (5, 'வியாழக்கிழமை'),
            (6, 'வெள்ளிக்கிழமை'),
            (7, 'சனிக்கிழமை'),
        ]
        for order, name in tamil_days:
            TamilDay.objects.get_or_create(name=name, defaults={'order': order})

        # ── Own House ──
        for order, code, name in [
            (1, 'yes', 'உண்டு'),
            (2, 'no',  'இல்லை'),
        ]:
            OwnHouse.objects.get_or_create(code=code, defaults={'name': name, 'order': order})


        # ── Birth Order 1-10 ──
        for i in range(1, 11):
            BirthOrder.objects.get_or_create(name=str(i), defaults={'order': i})


        # ── Complexion ──
        for i, name in enumerate(['மாநிறம்','கோதுமை நிறம்','வெண்மை நிறம்','கருப்பு நிறம்','சிவப்பு நிறம்'], 1):
            Complexion.objects.get_or_create(name=name, defaults={'order': i})

        # ── Height 4.1 to 7.0 ──
        heights = []
        for feet in range(4, 8):
            max_inch = 12 if feet < 7 else 1
            for inch in range(0, max_inch):
                heights.append(f"{feet}.{inch:02d}")
        for i, h in enumerate(heights, 1):
            Height.objects.get_or_create(name=h, defaults={'order': i})

        # ── Caste & SubCaste ──
        caste_data = {
            'வன்னியர்': ['படையாட்சி','கவுண்டர்','வன்னியர்','பல்லி வன்னியர்','நல்லி வன்னியர்','பாடி வன்னியர்']
        }
        for caste_name, sub_castes in caste_data.items():
            caste, _ = Caste.objects.get_or_create(name=caste_name)
            for i, sc in enumerate(sub_castes, 1):
                SubCaste.objects.get_or_create(name=sc, caste=caste, defaults={'order': i})

        self.stdout.write(self.style.SUCCESS('✅ All lookup data loaded successfully!'))
