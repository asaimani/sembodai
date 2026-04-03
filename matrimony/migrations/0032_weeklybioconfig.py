from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0031_marriedcandidate'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyBioConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('bio_token_expiry_days', models.PositiveIntegerField(default=30, verbose_name='பயோ இணைப்பு காலம் (நாட்கள்)')),
                ('married_cleanup_days', models.PositiveIntegerField(default=90, verbose_name='திருமணமான வரன் தக்க வைப்பு (நாட்கள்)')),
                ('bio_log_retention_days', models.PositiveIntegerField(default=365, verbose_name='அனுப்பல் பதிவு தக்க வைப்பு (நாட்கள்)')),
                ('default_weekly_limit', models.PositiveIntegerField(default=5, verbose_name='இயல்புநிலை வார வரம்பு')),
                ('remarriage_silver_limit', models.PositiveIntegerField(default=5, verbose_name='மறுமணம் Silver வார வரம்பு')),
                ('remarriage_gold_limit', models.PositiveIntegerField(default=10, verbose_name='மறுமணம் Gold வார வரம்பு')),
                ('remarriage_platinum_limit', models.PositiveIntegerField(default=20, verbose_name='மறுமணம் Platinum வார வரம்பு')),
                ('remarriage_diamond_limit', models.PositiveIntegerField(default=0, verbose_name='மறுமணம் Diamond வார வரம்பு (0=வரம்பற்றது)')),
                ('match_age_strict', models.BooleanField(default=True, verbose_name='வயது பொருத்தம் கட்டாயம்')),
                ('match_divorced_only', models.BooleanField(default=True, verbose_name='மறுமணம் ↔ மறுமணம் மட்டும்')),
                ('max_receivers_per_run', models.PositiveIntegerField(default=50, verbose_name='ஒரு இயக்கத்தில் அதிகபட்ச பெறுபவர்கள்')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={'verbose_name': 'வார அனுப்பல் அமைப்பு'},
        ),
    ]
