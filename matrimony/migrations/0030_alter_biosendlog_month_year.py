from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0029_weeklybiorun_weekly_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biosendlog',
            name='month_year',
            field=models.CharField(max_length=10, verbose_name='வார தொடக்கம்'),
        ),
    ]
