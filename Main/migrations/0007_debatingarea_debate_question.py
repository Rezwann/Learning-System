# Generated by Django 4.1.4 on 2023-04-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_debatingarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='debatingarea',
            name='debate_question',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
