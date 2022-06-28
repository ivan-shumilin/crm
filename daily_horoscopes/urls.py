from django.urls import path, re_path, include


from . import views

urlpatterns = [
    # path('api/forecast/', views.GetForecastInfoView.as_view()),
    path('', views.index, name='index'),
    path('test/', views.index1, name='index1'),
    # path('test/', views.index1, name='index1'),
    # path('form/', views.form, name='form'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
]
