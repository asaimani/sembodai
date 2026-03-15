from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0022_remove_femalecandidate_navamsam_h1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='malecandidate',
            name='old_reg_no',
            field=models.CharField(blank=True, max_length=50, verbose_name='ஒ.பதிவு எண்'),
        ),
        migrations.AddField(
            model_name='femalecandidate',
            name='old_reg_no',
            field=models.CharField(blank=True, max_length=50, verbose_name='ஒ.பதிவு எண்'),
        ),
    ]
