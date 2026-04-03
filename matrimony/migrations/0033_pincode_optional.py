from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0032_weeklybioconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='malecandidate',
            name='pincode',
            field=models.CharField(blank=True, max_length=10, verbose_name='பின்கோட்'),
        ),
        migrations.AlterField(
            model_name='femalecandidate',
            name='pincode',
            field=models.CharField(blank=True, max_length=10, verbose_name='பின்கோட்'),
        ),
    ]
