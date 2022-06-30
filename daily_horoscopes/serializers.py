import io

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd', 'vbd', 'nbd', 'nkd',
            'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category')
