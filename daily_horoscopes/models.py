from django.db import models
from datetime import date
import uuid


class Base(models.Model):
    date_create = models.DateField(default=date.today)
    base = models.CharField(max_length=5000000, null=True)

    def __str__(self):
        return f'{self.base}'


class Product(models.Model):
    iditem = models.IntegerField(null=True)
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
    ovd_sugarless = models.BooleanField(null=True)
    shd = models.BooleanField(null=True)
    bd = models.BooleanField(null=True)
    vbd = models.BooleanField(null=True)
    nbd = models.BooleanField(null=True)
    nkd = models.BooleanField(null=True)
    vkd = models.BooleanField(null=True)
    category = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return f'{self.name}, {self.category}'
#

class Timetable(models.Model):
    datetime = models.DateField()
    item = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    date_create = models.DateField(default=date.today, null=True)
    def __str__(self):
        return f'{self.item}'
#
# class Patient(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     LOAN_STATUS = (
#         ('ОВД', 'ОВД'),
#         ('ЩД', 'ЩД'),
#         ('БД', 'БД'),
#         ('ВКД', 'ВКД'),
#     )
#
#     type_of_diet = models.CharField(
#         max_length=1,
#         choices=LOAN_STATUS,
#         blank=True,
#         default='ОВД',
#         help_text='Book availability')
#
#     def __str__(self):
#         return f'{self.item}'
