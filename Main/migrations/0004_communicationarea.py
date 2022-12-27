# Generated by Django 4.1.4 on 2022-12-27 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_customuser_subjects_subject_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.subject')),
            ],
        ),
    ]
