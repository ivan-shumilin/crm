from django.contrib import admin
from .models import Menu, Base, Product


admin.site.register(Base)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')

    fields = ('ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')


admin.site.register(Product, ProductAdmin)
