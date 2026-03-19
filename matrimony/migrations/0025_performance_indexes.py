from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0024_ragukethu'),
    ]

    operations = [
        # MaleCandidate indexes
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['is_paid'], name='male_is_paid_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['is_paid', 'created_at'], name='male_paid_created_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['name'], name='male_name_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['uid'], name='male_uid_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['old_reg_no'], name='male_old_reg_no_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['rasi'], name='male_rasi_idx'),
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
            index=models.Index(fields=['monthly_salary'], name='male_salary_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['premium_end_date'], name='male_premium_end_idx'),
        ),
        migrations.AddIndex(
            model_name='malecandidate',
            index=models.Index(fields=['created_at'], name='male_created_at_idx'),
        ),

        # FemaleCandidate indexes
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['is_paid'], name='female_is_paid_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['is_paid', 'created_at'], name='female_paid_created_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['name'], name='female_name_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['uid'], name='female_uid_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['old_reg_no'], name='female_old_reg_no_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['rasi'], name='female_rasi_idx'),
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
            index=models.Index(fields=['monthly_salary'], name='female_salary_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['premium_end_date'], name='female_premium_end_idx'),
        ),
        migrations.AddIndex(
            model_name='femalecandidate',
            index=models.Index(fields=['created_at'], name='female_created_at_idx'),
        ),
    ]
