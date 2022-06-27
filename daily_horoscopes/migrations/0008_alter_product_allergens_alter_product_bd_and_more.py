# Generated by Django 4.0.3 on 2022-06-27 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0007_alter_product_ovd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='allergens',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='bd',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='carbohydrate',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='energy',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='fat',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='fiber',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='gluten_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='lactose_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='nbd',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='nkd',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='ovd',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='shd',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='sugarless',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='vbd',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='vegan',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='vkd',
            field=models.BooleanField(default=False),
        ),
    ]
