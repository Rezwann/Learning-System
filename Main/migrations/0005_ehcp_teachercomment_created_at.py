# Generated by Django 4.1.4 on 2023-04-13 13:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_alter_ehcp_aspiration_student_aspirations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ehcp_teachercomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
