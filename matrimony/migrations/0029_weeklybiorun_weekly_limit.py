from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0028_remove_candidateexpectation_unique_candidate_expectation_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        # 1. Rename monthly_limit to weekly_limit on PremiumType
        migrations.RenameField(
            model_name='premiumtype',
            old_name='monthly_limit',
            new_name='weekly_limit',
        ),

        # 2. Update limits: Silver=5, Gold=10, Platinum=20, Diamond=0
        migrations.RunSQL(
            """
            UPDATE matrimony_premiumtype SET weekly_limit=5  WHERE code='silver';
            UPDATE matrimony_premiumtype SET weekly_limit=10 WHERE code='gold';
            UPDATE matrimony_premiumtype SET weekly_limit=20 WHERE code='platinum';
            UPDATE matrimony_premiumtype SET weekly_limit=0  WHERE code='diamond';
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 3. Create WeeklyBioRun table
        migrations.CreateModel(
            name='WeeklyBioRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('run_at', models.DateTimeField(auto_now_add=True, verbose_name='இயக்கிய நேரம்')),
                ('week_start', models.DateField(verbose_name='வார தொடக்கம் (ஞாயிறு)')),
                ('week_end', models.DateField(verbose_name='வார முடிவு (சனி)')),
                ('male_processed', models.PositiveIntegerField(default=0, verbose_name='ஆண் விண்ணப்பதாரர்கள்')),
                ('female_processed', models.PositiveIntegerField(default=0, verbose_name='பெண் விண்ணப்பதாரர்கள்')),
                ('matches_created', models.PositiveIntegerField(default=0, verbose_name='பொருத்தங்கள் உருவாக்கப்பட்டன')),
                ('notes', models.TextField(blank=True, verbose_name='குறிப்புகள்')),
                ('run_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='auth.user',
                    verbose_name='இயக்கியவர்'
                )),
            ],
            options={
                'verbose_name': 'வார இயக்க பதிவு',
                'ordering': ['-run_at'],
            },
        ),
    ]
