from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Forecast
from .forms import UserRegistrationForm, UserloginForm

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ForecastSerializer
import calendar, datetime

import json

from django.db import transaction
from django.utils.dateparse import parse_date
import requests


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login



@transaction.atomic  # инструмент управления транзакциями базы данных
def load_forecast():
    Forecast.objects.all().delete()  # очищаем базу данных перед тем как заполнить таблицу
    forecasts = parsing()
    to_create = []  # список объектов
    for forecast in forecasts:
        to_create.append(Forecast(
            sing=forecast['sing'],
            description=forecast['description'],
        ))
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-create
    # вставляет предоставленный список объектов в базу данных (обычно только 1 запрос, независимо от того, сколько объектов имеется)
    Forecast.objects.bulk_create(to_create)

class BaseAPIView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        with open('data.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
        return Response(data)


class GetForecastInfoView(APIView):

    def get(self, request):
        # если в базе есть запись созданная сегодня берем данные с модели
        # если нет парсим и записываем новые данные в модель
        if have_forecast_today():
            queryset = Forecast.objects.all()
        else:
            # парсим и записываем
            load_forecast()
            queryset = Forecast.objects.all()
        # Сериализуем данныеа
        serializer_for_queryset = ForecastSerializer(queryset, many=True).data
        return Response(serializer_for_queryset)


def index(request):
    """ Функция для отображения главной страницы. """
    context = {'today': datetime.date.today(), }
    return render(request=request, template_name='index.html', context=context)


def register(request):
    """ Регистрация нового пользователя"""
    errors = []
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # делаем запрос на регистрацию нового пользователя (DRF)
            url = 'https://intense-badlands-65950.herokuapp.com/api/v1/auth/users/'
            headers = {'content-type': 'application/json'}
            payload = {
                'email': user_form.cleaned_data['email'],
                'username': user_form.cleaned_data['username'],
                'password': user_form.cleaned_data['password'],
            }
            response = requests.post(url, headers=headers, json=payload).json()

            if payload['username'] == response.get('username'):  # если имя пользователя есть в ответе регестрация прошла успешно
                return render(request, 'registration/register_done.html', {'new_user': user_form.cleaned_data})
            else:
                errors = list(response.values())
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'errors': errors})


def get_token(username, password):
    response = {
        'token': None,
        'error': None
    }
    url = 'https://intense-badlands-65950.herokuapp.com/auth/token/login/'
    headers = {'content-type': 'application/json'}
    payload = {
        'username': username,
        'password': password,

    }
    response_on_json = requests.post(url, headers=headers, json=payload)
    response_on_python = response_on_json.json()
    if response_on_python.get("auth_token"):
        if len(response_on_python["auth_token"]) != 40:
            response['error'] = response_on_python["auth_token"]
        else:
            response['token'] = response_on_python["auth_token"]
    return response


def user_login(request):
    errors = None
    if request.method == 'POST':
        user_form = UserloginForm(request.POST)
        user = authenticate(username=user_form.data['username'],
                            password=user_form.data['password'])
        if user is not None:
            login(request, user)
            response = get_token(user_form.data['username'], user_form.data['password'])
            return render(request, 'profile.html',
                          {'new_user': user_form.data, 'response': response})
        else:
            errors = 'Пользователя с таким именем и паролем не существует'
    else:
        user_form = UserloginForm()
    return render(request, 'registration/login.html', {'user_form': user_form,
                                                       'errors': errors})


def profile(request):
    return render(
        request=request,
        template_name='profile.html',
        context=context
    )
