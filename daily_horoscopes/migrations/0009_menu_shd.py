# Generated by Django 4.0.3 on 2022-06-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0008_menu_ovd'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='shd',
            field=models.BooleanField(null=True),
        ),
    ]