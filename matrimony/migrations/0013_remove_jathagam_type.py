from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('matrimony', '0012_state_order'),
    ]
    operations = [
        migrations.RemoveField(
            model_name='malecandidate',
            name='jathagam_type',
        ),
        migrations.RemoveField(
            model_name='femalecandidate',
            name='jathagam_type',
        ),
    ]
