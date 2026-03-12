from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('matrimony', '0011_alter_subcaste_options_and_more'),
    ]
    operations = [
        migrations.AddField(
            model_name='state',
            name='order',
            field=models.IntegerField(default=99),
        ),
        migrations.AddField(
            model_name='district',
            name='order',
            field=models.IntegerField(default=99),
        ),
    ]
