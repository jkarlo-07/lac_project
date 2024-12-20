# Generated by Django 5.1.1 on 2024-11-08 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_roomtype_cottage_price_roomtype_is_cottage_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='adult_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='is_overnight',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='kid_count',
            field=models.IntegerField(default=0),
        ),
    ]
