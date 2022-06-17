from django.contrib import admin
from .models import Menu
from rest_framework.authtoken.admin import TokenAdmin

admin.site.register(Menu)
TokenAdmin.raw_id_fields = ['user']
