# Generated by Django 4.1.4 on 2023-04-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_customuser_averagecd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opinion',
            name='thumbs_down',
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='thumbs_up',
        ),
        migrations.AlterField(
            model_name='subject',
            name='details',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
    ]
