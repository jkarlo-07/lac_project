# Generated by Django 5.1.1 on 2024-11-12 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0022_seasonaldata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seasonaldata',
            name='off_peak_months',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='seasonaldata',
            name='peak_months',
            field=models.JSONField(default=list),
        ),
    ]
