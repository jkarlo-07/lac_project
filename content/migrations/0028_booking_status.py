# Generated by Django 5.1.1 on 2024-11-15 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0027_roomtype_base_price_alter_roomtype_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(default='Booked', max_length=10),
        ),
    ]
