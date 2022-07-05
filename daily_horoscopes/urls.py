from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('backup/', views.backup, name='backup'),
    path('accounts/login/', views.user_login, name='login'),
]
