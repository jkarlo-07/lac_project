# Generated by Django 5.1.1 on 2024-11-08 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_booking_adult_count_booking_is_overnight_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='adult_count',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='is_overnight',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='kid_count',
        ),
    ]
