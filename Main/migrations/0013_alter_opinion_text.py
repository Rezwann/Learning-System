# Generated by Django 4.1.4 on 2023-05-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_alter_opinion_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='text',
            field=models.CharField(blank=True, default='No text was given.', max_length=255),
        ),
    ]