# Generated by Django 4.0.3 on 2022-06-27 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0008_alter_product_allergens_alter_product_bd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='allergens',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='bd',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='carbohydrate',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=1000, null=True),
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
        migrations.AlterField(
            model_name='product',
            name='gluten_free',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='lactose_free',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='nbd',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='nkd',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='ovd',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='shd',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sugarless',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='vbd',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='vegan',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='vkd',
            field=models.BooleanField(null=True),
        ),
    ]
