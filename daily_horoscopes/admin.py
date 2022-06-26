from django.contrib import admin
from .models import Base, Product
# from .models import Base, Product, Timetable


admin.site.register(Base)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')
    fields = ('ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd', 'vkd')
    # list_filter = ('status', 'due_back')

# class TimetableAdmin(admin.ModelAdmin):
#     list_display = ('item', 'datetime',)
#
#
# admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Product, ProductAdmin)
