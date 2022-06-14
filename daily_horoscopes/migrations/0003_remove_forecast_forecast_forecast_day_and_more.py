# Generated by Django 4.0.3 on 2022-03-09 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0002_alter_forecast_forecast'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forecast',
            name='forecast',
        ),
        migrations.AddField(
            model_name='forecast',
            name='day',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='forecast',
            name='description',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
