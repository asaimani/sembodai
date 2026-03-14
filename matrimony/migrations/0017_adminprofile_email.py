from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('matrimony', '0016_adminprofile_address_line3'),
    ]
    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='மின்னஞ்சல்'),
        ),
    ]
