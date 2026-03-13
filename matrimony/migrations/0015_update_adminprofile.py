from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('matrimony', '0014_alter_district_options_alter_state_options_and_more'),
    ]
    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='address_line1',
            field=models.CharField(blank=True, max_length=200, verbose_name='முகவரி வரி 1'),
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='address_line2',
            field=models.CharField(blank=True, max_length=200, verbose_name='முகவரி வரி 2'),
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='alternate_phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='மாற்று தொலைபேசி'),
        ),
        migrations.RemoveField(
            model_name='adminprofile',
            name='address',
        ),
    ]
