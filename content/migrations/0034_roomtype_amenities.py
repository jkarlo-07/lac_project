# Generated by Django 5.1.1 on 2025-01-17 13:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0033_amenities'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='amenities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None),
        ),
    ]
