from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0018_adminprofile_email_and_more'),
    ]

    operations = [
        # Rename TamilDay table to TamilKizhamai
        migrations.RenameModel('TamilDay', 'TamilKizhamai'),

        # Update verbose_name
        migrations.AlterModelOptions(
            name='tamilkizhamai',
            options={'ordering': ['order'], 'verbose_name': 'தமிழ் கிழமை'},
        ),

        # Rename FK field in male/female candidate
        migrations.RenameField('malecandidate', 'tamil_day', 'tamil_kizhamai'),
        migrations.RenameField('femalecandidate', 'tamil_day', 'tamil_kizhamai'),

        # Create TamilDate model
        migrations.CreateModel(
            name='TamilDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='தமிழ் தேதி')),
                ('order', models.PositiveIntegerField(default=99)),
            ],
            options={'verbose_name': 'தமிழ் தேதி', 'ordering': ['order']},
        ),

        # Add tamil_date FK to candidates
        migrations.AddField(
            model_name='malecandidate',
            name='tamil_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='matrimony.tamildate', verbose_name='தமிழ் தேதி'),
        ),
        migrations.AddField(
            model_name='femalecandidate',
            name='tamil_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='matrimony.tamildate', verbose_name='தமிழ் தேதி'),
        ),
    ]
