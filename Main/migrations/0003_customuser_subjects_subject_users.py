# Generated by Django 4.1.4 on 2022-12-27 16:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_alter_learningboard_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='subjects',
            field=models.ManyToManyField(to='Main.subject'),
        ),
        migrations.AddField(
            model_name='subject',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
