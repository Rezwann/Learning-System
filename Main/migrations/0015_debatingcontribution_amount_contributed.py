# Generated by Django 4.1.4 on 2023-05-04 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0014_remove_debatingcontribution_amount_contributed'),
    ]

    operations = [
        migrations.AddField(
            model_name='debatingcontribution',
            name='amount_contributed',
            field=models.IntegerField(default=0),
        ),
    ]
