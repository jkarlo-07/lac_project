# Generated by Django 5.1.1 on 2024-11-12 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_alter_seasonaldata_off_peak_months_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seasonaldata',
            name='year',
        ),
        migrations.AddField(
            model_name='seasonaldata',
            name='years',
            field=models.JSONField(default=list),
        ),
    ]
