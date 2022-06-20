from django.contrib import admin
from .models import Menu, Base
from rest_framework.authtoken.admin import TokenAdmin

admin.site.register(Menu)
admin.site.register(Base)
TokenAdmin.raw_id_fields = ['user']
