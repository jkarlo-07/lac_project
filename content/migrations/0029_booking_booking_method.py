# Generated by Django 5.1.1 on 2024-11-20 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0028_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_method',
            field=models.CharField(default='online', max_length=15),
        ),
    ]
