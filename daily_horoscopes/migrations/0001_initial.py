# Generated by Django 4.0.3 on 2022-06-26 13:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateField(default=datetime.date.today)),
                ('base', models.CharField(max_length=5000000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iditem', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.IntegerField(null=True)),
                ('carbohydrate', models.CharField(max_length=200, null=True)),
                ('fat', models.CharField(max_length=200, null=True)),
                ('fiber', models.CharField(max_length=200, null=True)),
                ('energy', models.CharField(max_length=200, null=True)),
                ('image', models.CharField(max_length=2000, null=True)),
                ('vegan', models.BooleanField(null=True)),
                ('allergens', models.BooleanField(null=True)),
                ('lactose_free', models.BooleanField(null=True)),
                ('sugarless', models.BooleanField(null=True)),
                ('gluten_free', models.BooleanField(null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('ovd', models.BooleanField(null=True)),
                ('shd', models.BooleanField(null=True)),
                ('bd', models.BooleanField(null=True)),
                ('vbd', models.BooleanField(null=True)),
                ('nbd', models.BooleanField(null=True)),
                ('nkd', models.BooleanField(null=True)),
                ('vkd', models.BooleanField(null=True)),
                ('category', models.CharField(max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateField()),
                ('date_create', models.DateField(default=datetime.date.today, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='daily_horoscopes.product')),
            ],
        ),
    ]
