from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0026_premium_type'),
    ]

    operations = [
        # 1. Add monthly_limit to PremiumType
        migrations.AddField(
            model_name='premiumtype',
            name='monthly_limit',
            field=models.PositiveIntegerField(default=5, verbose_name='மாத வரம்பு (0=வரம்பற்றது)'),
        ),

        # 2. Set limits: Silver=5, Gold=10, Platinum=20, Diamond=0(unlimited)
        migrations.RunSQL(
            """
            UPDATE matrimony_premiumtype SET monthly_limit=5  WHERE code='silver';
            UPDATE matrimony_premiumtype SET monthly_limit=10 WHERE code='gold';
            UPDATE matrimony_premiumtype SET monthly_limit=20 WHERE code='platinum';
            UPDATE matrimony_premiumtype SET monthly_limit=0  WHERE code='diamond';
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 3. CandidateExpectation
        migrations.CreateModel(
            name='CandidateExpectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('candidate_gender', models.CharField(choices=[('M', 'ஆண்'), ('F', 'பெண்')], max_length=1, verbose_name='பாலினம்')),
                ('candidate_id', models.PositiveIntegerField(verbose_name='விண்ணப்பதாரர் ID')),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='குறைந்த சம்பளம்')),
                ('education_min', models.CharField(blank=True, max_length=200, verbose_name='கல்வித் தகுதி')),
                ('job_type', models.CharField(choices=[('any', 'எதுவும்'), ('govt', 'அரசு'), ('private', 'தனியார்'), ('business', 'வியாபாரம்')], default='any', max_length=20, verbose_name='வேலை வகை')),
                ('notes', models.TextField(blank=True, verbose_name='குறிப்புகள்')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sevadosham_ok', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='matrimony.sevadosham', verbose_name='செவ்வாய் தோஷம்')),
                ('own_house_pref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='matrimony.ownhouse', verbose_name='சொந்த வீடு')),
                ('marital_status_ok', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='matrimony.maritalstatus', verbose_name='திருமண நிலை')),
            ],
            options={'verbose_name': 'எதிர்பார்ப்பு'},
        ),
        migrations.AddConstraint(
            model_name='candidateexpectation',
            constraint=models.UniqueConstraint(fields=['candidate_gender', 'candidate_id'], name='unique_candidate_expectation'),
        ),

        # 4. Many-to-many expectation tables
        migrations.CreateModel(
            name='ExpectationNachathiram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('expectation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nachathirams', to='matrimony.candidateexpectation')),
                ('nachathiram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrimony.nachathiram', verbose_name='நட்சத்திரம்')),
            ],
            options={'unique_together': {('expectation', 'nachathiram')}},
        ),
        migrations.CreateModel(
            name='ExpectationSubCaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('expectation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_castes', to='matrimony.candidateexpectation')),
                ('sub_caste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrimony.subcaste', verbose_name='உட்பிரிவு')),
            ],
            options={'unique_together': {('expectation', 'sub_caste')}},
        ),
        migrations.CreateModel(
            name='ExpectationDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('expectation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='matrimony.candidateexpectation')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrimony.district', verbose_name='மாவட்டம்')),
            ],
            options={'unique_together': {('expectation', 'district')}},
        ),
        migrations.CreateModel(
            name='ExpectationProfession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('expectation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professions', to='matrimony.candidateexpectation')),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrimony.profession', verbose_name='தொழில்')),
            ],
            options={'unique_together': {('expectation', 'profession')}},
        ),
        migrations.CreateModel(
            name='ExpectationComplexion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('expectation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complexions', to='matrimony.candidateexpectation')),
                ('complexion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrimony.complexion', verbose_name='நிறம்')),
            ],
            options={'unique_together': {('expectation', 'complexion')}},
        ),

        # 5. BioToken
        migrations.CreateModel(
            name='BioToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=64, unique=True, verbose_name='டோக்கன்')),
                ('candidate_gender', models.CharField(choices=[('M', 'ஆண்'), ('F', 'பெண்')], max_length=1)),
                ('candidate_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(verbose_name='காலாவதி தேதி')),
            ],
            options={'verbose_name': 'பயோ டோக்கன்'},
        ),
        migrations.AddIndex(
            model_name='biotoken',
            index=models.Index(fields=['token'], name='bio_token_idx'),
        ),

        # 6. BioSendLog
        migrations.CreateModel(
            name='BioSendLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('sender_gender', models.CharField(choices=[('M', 'ஆண்'), ('F', 'பெண்')], max_length=1, verbose_name='அனுப்புபவர் பாலினம்')),
                ('sender_id', models.PositiveIntegerField(verbose_name='அனுப்புபவர் ID')),
                ('receiver_gender', models.CharField(choices=[('M', 'ஆண்'), ('F', 'பெண்')], max_length=1, verbose_name='பெறுபவர் பாலினம்')),
                ('receiver_id', models.PositiveIntegerField(verbose_name='பெறுபவர் ID')),
                ('month_year', models.CharField(max_length=7, verbose_name='மாதம்-வருடம்')),
                ('status', models.CharField(choices=[('pending', 'நிலுவை'), ('sent', 'அனுப்பியது'), ('failed', 'தோல்வி')], default='pending', max_length=10)),
                ('prepared_at', models.DateTimeField(auto_now_add=True, verbose_name='தயாரித்த நேரம்')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='அனுப்பிய நேரம்')),
                ('bio_token', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='matrimony.biotoken')),
            ],
            options={'verbose_name': 'அனுப்பல் பதிவு', 'ordering': ['-prepared_at']},
        ),
        migrations.AddIndex(
            model_name='biosendlog',
            index=models.Index(fields=['sender_gender', 'sender_id', 'month_year'], name='biosend_sender_idx'),
        ),
        migrations.AddIndex(
            model_name='biosendlog',
            index=models.Index(fields=['sender_gender', 'sender_id', 'receiver_gender', 'receiver_id'], name='biosend_pair_idx'),
        ),
    ]
