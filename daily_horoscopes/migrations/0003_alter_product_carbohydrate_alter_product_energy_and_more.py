# Generated by Django 4.0.3 on 2022-06-21 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0002_product_delete_forecast'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='carbohydrate',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='energy',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='fat',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='fiber',
            field=models.CharField(max_length=200, null=True),
        ),
    ]