from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0023_add_old_reg_no'),
    ]

    operations = [
        # 1. Create RaguKethu table
        migrations.CreateModel(
            name='RaguKethu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='குறியீடு')),
                ('name', models.CharField(max_length=50, verbose_name='பெயர்')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'ராகு/கேது',
                'ordering': ['order'],
            },
        ),

        # 2. Clear ragu_kethu on MaleCandidate before changing FK
        migrations.RunSQL(
            "UPDATE matrimony_malecandidate SET ragu_kethu_id = NULL;",
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 3. Clear ragu_kethu on FemaleCandidate before changing FK
        migrations.RunSQL(
            "UPDATE matrimony_femalecandidate SET ragu_kethu_id = NULL;",
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 4. Change ragu_kethu FK on MaleCandidate to RaguKethu
        migrations.AlterField(
            model_name='malecandidate',
            name='ragu_kethu',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='+',
                to='matrimony.ragukethu',
                verbose_name='ராகு/கேது',
            ),
        ),

        # 5. Change ragu_kethu FK on FemaleCandidate to RaguKethu
        migrations.AlterField(
            model_name='femalecandidate',
            name='ragu_kethu',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='+',
                to='matrimony.ragukethu',
                verbose_name='ராகு/கேது',
            ),
        ),
    ]
