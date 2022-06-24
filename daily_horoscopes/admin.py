from django.contrib import admin
from .models import Base, Product, Timetable


admin.site.register(Base)
admin.site.register(Timetable)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')

    fields = ('ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')


admin.site.register(Product, ProductAdmin)
