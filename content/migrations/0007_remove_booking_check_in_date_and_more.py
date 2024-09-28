# Generated by Django 5.1.1 on 2024-09-28 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_guest_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='check_in_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='check_out_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='start_time',
        ),
        migrations.AddField(
            model_name='booking',
            name='check_in',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 28, 8, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='check_out',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 28, 20, 0)),
            preserve_default=False,
        ),
    ]
