# Generated by Django 5.1.1 on 2024-11-12 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_rename_based_price_roomtype_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=1500, max_digits=10),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
