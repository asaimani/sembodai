from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('matrimony', '0015_update_adminprofile'),
    ]
    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='address_line3',
            field=models.CharField(blank=True, max_length=200, verbose_name='முகவரி வரி 3'),
        ),
    ]
