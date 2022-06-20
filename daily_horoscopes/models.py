from django.db import models
from datetime import date
import uuid

# Create your models here.
class Forecast(models.Model):
    # forecast = models.CharField(max_length=5000)
    sing = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=5000, null=True)
    date_create = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.sing} - {self.description}'


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
