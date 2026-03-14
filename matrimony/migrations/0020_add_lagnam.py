from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0019_rename_tamilday_add_tamildate'),
    ]

    operations = [
        # Fix rasi related_name first
        migrations.AlterField(
            model_name='malecandidate',
            name='rasi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='matrimony.rasi', verbose_name='ராசி'),
        ),
        migrations.AlterField(
            model_name='femalecandidate',
            name='rasi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='matrimony.rasi', verbose_name='ராசி'),
        ),
        # Add lagnam to male
        migrations.AddField(
            model_name='malecandidate',
            name='lagnam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='matrimony.rasi', verbose_name='லக்னம்'),
        ),
        # Add lagnam to female
        migrations.AddField(
            model_name='femalecandidate',
            name='lagnam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='matrimony.rasi', verbose_name='லக்னம்'),
        ),
    ]
