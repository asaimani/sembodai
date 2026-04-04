from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0033_pincode_optional'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('create', 'சேர்க்கப்பட்டது'), ('update', 'திருத்தப்பட்டது'), ('delete', 'நீக்கப்பட்டது'), ('status', 'நிலை மாற்றம்'), ('premium', 'பிரீமியம் மாற்றம்')], max_length=10)),
                ('gender', models.CharField(max_length=1)),
                ('candidate_id', models.PositiveIntegerField()),
                ('candidate_uid', models.CharField(blank=True, max_length=20)),
                ('candidate_name', models.CharField(blank=True, max_length=200)),
                ('details', models.TextField(blank=True)),
                ('performed_at', models.DateTimeField(auto_now_add=True)),
                ('performed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={'verbose_name': 'தணிக்கை பதிவு', 'ordering': ['-performed_at']},
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['gender', 'candidate_id'], name='audit_candidate_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['performed_at'], name='audit_time_idx'),
        ),
    ]
