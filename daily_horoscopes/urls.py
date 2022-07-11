from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/salad/<page>', views.catalog_salad, name='salad'),
    path('catalog/soup/<page>', views.catalog_soup, name='soup'),
    path('catalog/main_dishes/<page>', views.catalog_main_dishes, name='main_dishes'),
    path('catalog/side_dishes/<page>', views.catalog_side_dishes, name='side_dishes'),
    path('backup/', views.backup, name='backup'),
    path('accounts/login/', views.user_login, name='login'),
]
