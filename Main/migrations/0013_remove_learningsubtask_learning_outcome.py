# Generated by Django 4.1.4 on 2023-02-15 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_remove_userresponse_is_correct_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learningsubtask',
            name='learning_outcome',
        ),
    ]