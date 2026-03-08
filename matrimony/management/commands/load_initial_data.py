from django.core.management.base import BaseCommand
from matrimony.models import Rasi, Nachathiram, Profession, Jathagam, State, District

class Command(BaseCommand):
    help = 'Load initial lookup data'

    def handle(self, *args, **kwargs):
        # Rasi data
        rasis_data = [
            ('மேஷம்', ['அஸ்வினி', 'பரணி', 'கார்த்திகை 1']),
            ('ரிஷபம்', ['கார்த்திகை 2,3,4', 'ரோகிணி', 'மிருகசீரிடம் 1,2']),
            ('மிதுனம்', ['மிருகசீரிடம் 3,4', 'திருவாதிரை', 'புனர்பூசம் 1,2,3']),
            ('கடகம்', ['புனர்பூசம் 4', 'பூசம்', 'ஆயில்யம்']),
            ('சிம்மம்', ['மகம்', 'பூரம்', 'உத்திரம் 1']),
            ('கன்னி', ['உத்திரம் 2,3,4', 'அஸ்தம்', 'சித்திரை 1,2']),
            ('துலாம்', ['சித்திரை 3,4', 'சுவாதி', 'விசாகம் 1,2,3']),
            ('விருச்சிகம்', ['விசாகம் 4', 'அனுஷம்', 'கேட்டை']),
            ('தனுசு', ['மூலம்', 'பூராடம்', 'உத்திராடம் 1']),
            ('மகரம்', ['உத்திராடம் 2,3,4', 'திருவோணம்', 'அவிட்டம் 1,2']),
            ('கும்பம்', ['அவிட்டம் 3,4', 'சதயம்', 'பூரட்டாதி 1,2,3']),
            ('மீனம்', ['பூரட்டாதி 4', 'உத்திரட்டாதி', 'ரேவதி']),
        ]

        for rasi_name, natchathirams in rasis_data:
            rasi, _ = Rasi.objects.get_or_create(name=rasi_name)
            for n_name in natchathirams:
                Nachathiram.objects.get_or_create(name=n_name, defaults={'rasi': rasi})

        # Professions
        professions = [
            'விவசாயம்', 'அரசு ஊழியர்', 'தனியார் நிறுவனம்', 'வியாபாரம்',
            'மருத்துவர்', 'பொறியாளர்', 'ஆசிரியர்', 'வழக்கறிஞர்',
            'கணக்காளர்', 'காவல்துறை', 'இராணுவம்', 'கட்டுமான தொழில்',
            'வாகன தொழில்', 'நெசவு தொழில்', 'IT துறை', 'வங்கி துறை',
            'செவிலியர்', 'சமையல்காரர்', 'சிற்பி', 'பட்டதாரி வேலை இல்லாதவர்',
        ]
        for p in professions:
            Profession.objects.get_or_create(name=p)

        # Jathagam types
        jathagams = [
            'ஜாதகம் உள்ளது',
            'ஜாதகம் இல்லை',
            'கணினி ஜாதகம்',
            'கைப்படி ஜாதகம்',
            'சுவடி ஜாதகம்',
            'நாடி ஜாதகம்',
        ]
        for j in jathagams:
            Jathagam.objects.get_or_create(name=j)

        # Tamil Nadu Districts
        tn, _ = State.objects.get_or_create(name='தமிழ்நாடு')
        districts = [
            'சென்னை', 'கோயம்புத்தூர்', 'மதுரை', 'திருச்சிராப்பள்ளி',
            'சேலம்', 'திருநெல்வேலி', 'திருப்பூர்', 'வேலூர்',
            'ஈரோடு', 'தூத்துக்குடி', 'தஞ்சாவூர்', 'விருதுநகர்',
            'நீலகிரி', 'கடலூர்', 'விழுப்புரம்', 'நாமக்கல்',
            'கரூர்', 'திண்டுக்கல்', 'நாகப்பட்டினம்', 'புதுக்கோட்டை',
            'சிவகங்கை', 'ராமநாதபுரம்', 'கன்னியாகுமரி', 'வில்லுபுரம்',
            'திருவண்ணாமலை', 'கிருஷ்ணகிரி', 'தர்மபுரி', 'அரியலூர்',
            'பெரம்பலூர்', 'திருவாரூர்', 'தென்காசி', 'கள்ளக்குறிச்சி',
            'மயிலாடுதுறை', 'செங்கல்பட்டு', 'ரானிப்பேட்டை',
        ]
        for d in districts:
            District.objects.get_or_create(name=d, defaults={'state': tn})

        # Other states
        other_states = ['ஆந்திரப் பிரதேசம்', 'கர்நாடகா', 'கேரளா', 'மகாராஷ்டிரா', 'டெல்லி']
        for s in other_states:
            State.objects.get_or_create(name=s)

        self.stdout.write(self.style.SUCCESS('✅ அடிப்படை தரவு வெற்றிகரமாக சேர்க்கப்பட்டது!'))
