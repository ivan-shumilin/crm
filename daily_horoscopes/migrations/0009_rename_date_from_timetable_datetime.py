# Generated by Django 4.0.3 on 2022-06-24 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0008_timetable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='date_from',
            new_name='datetime',
        ),
    ]