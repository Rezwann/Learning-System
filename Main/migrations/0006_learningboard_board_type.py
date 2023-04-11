# Generated by Django 4.1.4 on 2023-04-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_alter_customuser_vocabulary_sheet_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningboard',
            name='board_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student', max_length=40),
        ),
    ]