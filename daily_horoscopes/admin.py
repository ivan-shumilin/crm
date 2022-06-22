from django.contrib import admin
from .models import Menu, Base, Product
from rest_framework.authtoken.admin import TokenAdmin

admin.site.register(Menu)
admin.site.register(Base)
# admin.site.register(Product)
TokenAdmin.raw_id_fields = ['user']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')

    fields = ('ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')


admin.site.register(Product, ProductAdmin)
