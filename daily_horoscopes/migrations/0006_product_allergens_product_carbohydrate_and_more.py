# Generated by Django 4.0.3 on 2022-06-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0005_remove_product_allergens_remove_product_carbohydrate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allergens',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='carbohydrate',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='energy',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='fat',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='fiber',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='gluten_free',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='lactose_free',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sugarless',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='vegan',
            field=models.BooleanField(null=True),
        ),
    ]
