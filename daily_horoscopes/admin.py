from django.contrib import admin
from .models import Base, Product, Timetable


admin.site.register(Base)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cooking_method', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category')
    fields = ('name', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'category', 'description')
    list_filter = ('category', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd', 'description')
    # list_filter = ('status', 'due_back')

class TimetableAdmin(admin.ModelAdmin):
    list_display = ('item', 'datetime',)
    list_filter = ('datetime',)


admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Product, ProductAdmin)
