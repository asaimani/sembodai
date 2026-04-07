from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0035_candidate_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklybioconfig',
            name='audit_log_retention_days',
            field=models.PositiveIntegerField(default=240, verbose_name='தணிக்கை பதிவு தக்க வைப்பு (நாட்கள்)'),
        ),
        migrations.AlterField(
            model_name='weeklybioconfig',
            name='married_cleanup_days',
            field=models.PositiveIntegerField(default=30, verbose_name='திருமணமான வரன் தக்க வைப்பு (நாட்கள்)'),
        ),
    ]
