# Generated by Django 4.0.3 on 2022-06-15 12:03

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0006_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='diet',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('ОВД', 'ОВД'), ('ЩД', 'ЩД'), ('БД', 'БД'), ('ВБД', 'ВБД')], max_length=20),
        ),
    ]