# Generated by Django 4.0.3 on 2022-06-16 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0009_menu_shd'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='bd',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='vbd',
            field=models.BooleanField(null=True),
        ),
    ]
