# Generated by Django 4.1.4 on 2022-12-28 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_alter_communicationarea_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images'),
        ),
    ]
