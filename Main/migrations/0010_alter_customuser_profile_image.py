# Generated by Django 4.1.4 on 2022-12-28 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/icon.png', null=True, upload_to='profile_images'),
        ),
    ]
