from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0030_alter_biosendlog_month_year'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarriedCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('M', 'ஆண்'), ('F', 'பெண்')], max_length=1)),
                ('candidate_id', models.PositiveIntegerField()),
                ('uid', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('married_at', models.DateTimeField(auto_now_add=True, verbose_name='திருமணம் பதிவு நேரம்')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=20)),
                ('whatsapp_number', models.CharField(blank=True, max_length=20)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='matrimony.district')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={
                'verbose_name': 'திருமணமான வரன்',
                'ordering': ['-married_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='marriedcandidate',
            unique_together={('gender', 'candidate_id')},
        ),
    ]
