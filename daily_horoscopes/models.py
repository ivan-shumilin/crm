from django.db import models
from datetime import date
import uuid

class Base(models.Model):
    date_create = models.DateField(default=date.today)
    base = models.CharField(max_length=50000000, null=True)

    def __str__(self):
        return f'{self.base}'


class Product(models.Model):
    id_item = models.IntegerField()
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    carbohydrate = models.CharField(max_length=200, null=True)
    fat = models.CharField(max_length=200, null=True)
    fiber = models.CharField(max_length=200, null=True)
    energy = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=2000, null=True)
    vegan = models.BooleanField(null=True)
    allergens = models.BooleanField(null=True)
    lactose_free = models.BooleanField(null=True)
    sugarless = models.BooleanField(null=True)
    gluten_free = models.BooleanField(null=True)
    description = models.CharField(max_length=1000, null=True)
    ovd = models.BooleanField(null=True)
    shd = models.BooleanField(null=True)
    bd = models.BooleanField(null=True)
    vbd = models.BooleanField(null=True)
    nbd = models.BooleanField(null=True)
    nkd = models.BooleanField(null=True)
    vkd = models.BooleanField(null=True)
    category = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return f'{self.name}, {self.category}'

# class Forecast(models.Model):
#     # forecast = models.CharField(max_length=5000)
#     sing = models.CharField(max_length=200, null=True)
#     description = models.CharField(max_length=5000, null=True)
#     date_create = models.DateField(default=date.today)
#
#     def __str__(self):
#         return f'{self.sing} - {self.description}'

#
#
class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=200, null=True)
    pfc = models.CharField(max_length=300, null=True)
    compound = models.CharField(max_length=300, null=True)

    ovd = models.BooleanField(null=True)
    shd = models.BooleanField(null=True)
    bd = models.BooleanField(null=True)
    vbd = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.title}'
#
# class Product(models.Model):
#     id = models.IntegerField(null=True)
#     name = models.CharField(max_length=200, null=True)
#     price = models.IntegerField(null=True)
#     carbohydrate = models.IntegerField(null=True)
#     fat = models.IntegerField(null=True)
#     fiber = models.IntegerField(null=True)
#     energy = models.IntegerField(null=True)
#     image = models.CharField(max_length=2000, null=True)
#     vegan = models.BooleanField(null=True)
#     allergens = models.BooleanField(null=True)
#     lactose_free = models.BooleanField(null=True)
#     sugarless = models.BooleanField(null=True)
#     gluten_free = models.BooleanField(null=True)
#     description = models.CharField(max_length=1000, null=True)
#     ovd = models.BooleanField(null=True)
#     shd = models.BooleanField(null=True)
#     bd = models.BooleanField(null=True)
#     vbd = models.BooleanField(null=True)
#     nbd = models.BooleanField(null=True)
#     nkd = models.BooleanField(null=True)
#     vkd = models.BooleanField(null=True)
#     category = models.CharField(max_length=2000, null=True)
#
#     def __str__(self):
#         return f'{self.id}, {self.name}, {self.category}'