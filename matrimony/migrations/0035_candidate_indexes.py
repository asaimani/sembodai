from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0034_auditlog'),
    ]

    operations = [
        # MaleCandidate indexes
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['status'], name='male_status_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['district'], name='male_district_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['premium_end_date'], name='male_premium_end_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['nachathiram'], name='male_nachathiram_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['date_of_birth'], name='male_dob_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['created_at'], name='male_created_idx'),
        ),
        # FemaleCandidate indexes
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['status'], name='female_status_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['district'], name='female_district_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['premium_end_date'], name='female_premium_end_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['nachathiram'], name='female_nachathiram_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['date_of_birth'], name='female_dob_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['created_at'], name='female_created_idx'),
        ),
    ]
