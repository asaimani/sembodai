from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0025_performance_indexes'),
    ]

    operations = [
        # 1. Create PremiumType table
        migrations.CreateModel(
            name='PremiumType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='குறியீடு')),
                ('name', models.CharField(max_length=50, verbose_name='பெயர்')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'பிரீமியம் வகை',
                'ordering': ['order'],
            },
        ),

        # 2. Seed Silver as default tier
        migrations.RunSQL(
            "INSERT INTO matrimony_premiumtype (code, name, \"order\") VALUES ('silver', 'Silver', 1);",
            reverse_sql="DELETE FROM matrimony_premiumtype WHERE code='silver';",
        ),

        # 3. Add premium_type FK to MaleCandidate (nullable)
        migrations.AddField(
            model_name='malecandidate',
            name='premium_type',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='matrimony.premiumtype',
                verbose_name='பிரீமியம் வகை',
            ),
        ),

        # 4. Add premium_type FK to FemaleCandidate (nullable)
        migrations.AddField(
            model_name='femalecandidate',
            name='premium_type',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='matrimony.premiumtype',
                verbose_name='பிரீமியம் வகை',
            ),
        ),

        # 5. Migrate all is_paid=True candidates → Silver
        migrations.RunSQL(
            """
            UPDATE matrimony_malecandidate
            SET premium_type_id = (SELECT id FROM matrimony_premiumtype WHERE code='silver')
            WHERE is_paid = TRUE;

            UPDATE matrimony_femalecandidate
            SET premium_type_id = (SELECT id FROM matrimony_premiumtype WHERE code='silver')
            WHERE is_paid = TRUE;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 6. Remove is_paid from MaleCandidate
        migrations.RemoveField(
            model_name='malecandidate',
            name='is_paid',
        ),

        # 7. Remove is_paid from FemaleCandidate
        migrations.RemoveField(
            model_name='femalecandidate',
            name='is_paid',
        ),

        # 8. Delete all shadow candidates data and drop table
        migrations.RunSQL(
            "DELETE FROM matrimony_shadowcandidate;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.DeleteModel(
            name='ShadowCandidate',
        ),
    ]
