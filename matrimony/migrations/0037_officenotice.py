from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0036_weeklybioconfig_audit_retention'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(default='கடந்த 30 ஆண்டுகளாக நம்பிக்கையான திருமண சேவையை வழங்கி வருகிறோம்.', max_length=300, verbose_name='வரி 1')),
                ('line2', models.CharField(default='பாதுகாப்பு கருதி, முகவரி இல்லாத சுயவிவரங்களை (Bio-data) மட்டும் அனுப்பியுள்ளோம்.', max_length=300, verbose_name='வரி 2')),
                ('line3', models.CharField(default='எங்கள் சேவையில் எவ்வித தரகு (Brokerage) அல்லது கமிஷன் (%) கட்டணமும் கண்டிப்பாக கிடையாது.', max_length=300, verbose_name='வரி 3')),
                ('line4', models.CharField(default='இந்த வரன் பிடித்திருந்தால், மேலும் விவரங்களுக்கு எங்களைத் தொடர்பு கொள்ளவும்.', max_length=300, verbose_name='வரி 4')),
                ('line5', models.CharField(default='அளவற்ற வரன்களின் விவரங்களை அன்போடு வழங்குகிறோம்; எங்கள் சந்தா 6 மாதத்திற்கு ₹2500 மட்டுமே.', max_length=300, verbose_name='வரி 5')),
            ],
            options={
                'verbose_name': 'முகவரி மறை அறிவிப்பு',
            },
        ),
    ]
