# Generated by Django 4.1.4 on 2023-04-03 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_customuser_vocabulary_sheet_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='vocabulary_sheet_group',
            field=models.CharField(choices=[('Very Low', 'Very Low'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Very High', 'Very High')], default='M', max_length=20),
        ),
    ]
