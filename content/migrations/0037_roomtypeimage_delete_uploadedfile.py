# Generated by Django 5.1.1 on 2025-01-17 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0036_uploadedfile_delete_roomimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomTypeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, default='', upload_to='room/')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.roomtype')),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]
