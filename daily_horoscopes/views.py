from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Base, Product, Timetable
from .forms import UserRegistrationForm, UserloginForm, TimetableForm
from django.forms import modelformset_factory
from .serializers import ProductSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import calendar, datetime
from datetime import datetime
from datetime import date
from django.template import RequestContext

import json

from django.db import transaction
from django.utils.dateparse import parse_date
import requests

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.forms import CheckboxInput, Textarea
from django.contrib.auth.decorators import login_required
import os
import requests
from rest_framework.renderers import JSONRenderer

URL = 'https://cloud-api.yandex.net/v1/disk/resources'
TOKEN = 'AQAAAAAnzmiwAAgF_TNw9en0lUKImDw8u7S2eQk'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}


def create_backup():
    queryset = Product.objects.all()
    serializer_for_queryset = ProductSerializer(queryset, many=True).data
    data = JSONRenderer().render(serializer_for_queryset).decode()
    name = str(date.today()) + '.json'
    with open(name, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def create_folder(path):
    """Создание папки. \n path: Путь к создаваемой папке."""
    requests.put(f'{URL}?path={path}', headers=headers)


def upload_file(loadfile, savefile, replace=False):
    """Загрузка файла.
    loadfile: Путь к загружаемому файлу
    savefile: Путь к файлу на Диске
    replace: true or false Замена файла на Диске"""

    res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file': f})
        except KeyError:
            print(res)


def backup(request):
    create_backup()
    create_folder('backup' + '/' + str(date.today()))
    upload_file(str(date.today()) + '.json', 'backup' + '/' + str(date.today()) + '/' + str(date.today()) + '.json')
    return render(request, 'backup.html', {})


@transaction.atomic
def load_menu(dict_tests):
    # Product.objects.all().delete()
    # Timetable.objects.all().delete()
    #
    # dict_tests = {'menu': {'id': 682, 'date': '24.06.2022', 'status': 'completed', 'completed_at': '22.06.2022 17:52:31', 'created_at': '17.06.2022 10:26:17', 'combo_price': 350, 'location': {'id': 4, 'name': 'hadassah', 'subdomain': 'hadassah'}, 'items': [{'id': 13276, 'combo': False, 'product': {'id': 251, 'name': 'Говядина по-азиатски 75/75 гр.', 'price': 239, 'carbohydrate': '0.57539', 'fat': '11.42332', 'fiber': '21.60205', 'energy': '191.51808', 'image': 'a8faed5c-fd3e-40cf-bb93-6d86240a268e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13277, 'combo': False, 'product': {'id': 337, 'name': 'Куриная ватрушка с грибным жульеном 120 гр.', 'price': 159, 'carbohydrate': '23.04720', 'fat': '17.42760', 'fiber': '20.17560', 'energy': '329.73120', 'image': '66366171-300e-469f-8692-de7da76785f4.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : Состав : фарш из курицы ( филе курицы, хлеб, соль, перекц , лук репчатый), масло подсолнечное, сыр Гауда, жульен грибной ( грибы шампиньоны, лук репчатый, масло подсолнечное, молоко 3,2%, сливки 33%, перец черный молотый, соль).'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13278, 'combo': False, 'product': {'id': 396, 'name': 'Перец фаршированный овощами, грибами и кус-кусом 200/50', 'price': 239, 'carbohydrate': '25.70250', 'fat': '8.97750', 'fiber': '4.95250', 'energy': '203.40750', 'image': '7bba3000-acb3-4b5d-aecd-aa0b7be477e5.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: перец болгарский, грибы шампиньоны, кускус, морковь, перец болгарский, томатный соус ( томатная паста, лук репчатый, морковь, перец черный молотый, соль, прованские травы),'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13279, 'combo': True, 'product': {'id': 1817, 'name': 'Суп-крем овощной 250 гр.', 'price': 99, 'carbohydrate': '21.50694', 'fat': '5.40708', 'fiber': '2.86319', 'energy': '146.14958', 'image': 'fb998852-3579-4a9a-bba7-abe5cccb8f32.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста брокколи, капуста цветная , лук репчатый, картофель, морковь, зхелень, сельдерей, перец, соль, масло оливковое, сливки 33 % .'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13280, 'combo': False, 'product': {'id': 1255, 'name': 'Тайский суп с лапшой и говядиной 250 гр.', 'price': 169, 'carbohydrate': '17.91500', 'fat': '14.48250', 'fiber': '15.07500', 'energy': '262.29000', 'image': '76113578-d361-41f9-9bad-31a37e26c856.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: шпинат, говядина, чеснок, имбирь, лук репчатый, морковь, масло подсолнечное, грибы шампиньоны, лапша гречневая, соевый соус, соль, перец.'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13281, 'combo': False, 'product': {'id': 434, 'name': 'Стейк из бедра индейки с томатной сальсой 100/50 гр.', 'price': 239, 'carbohydrate': '3.64950', 'fat': '16.14150', 'fiber': '21.92400', 'energy': '247.57050', 'image': 'df5fb311-1b7f-4373-bc4d-2ca869c8b3e7.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : филе индейки, соевый соус, тимьян, мед, масло подсолнечное, томатная сальса( помидор, лук репчатый, чеснок, кинза, соль, перец, масло оливковое).'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13282, 'combo': True, 'product': {'id': 446, 'name': 'Тефтели куриные с зеленым горошком в сметанном соусе 100/50гр.', 'price': 139, 'carbohydrate': '16.39800', 'fat': '12.20250', 'fiber': '14.38200', 'energy': '232.92450', 'image': '1b066181-48e5-4739-b847-6819afa21f54.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: фарш куриный (курица, соль, перец, лук, хлеб),горек зеленый, сметана, мука пшеничная, соль,перец черный молотый.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13283, 'combo': False, 'product': {'id': 514, 'name': 'Брокколи на пару с болгарским перцем 150 гр.', 'price': 119, 'carbohydrate': '7.41150', 'fat': '5.26650', 'fiber': '3.73650', 'energy': '91.98150', 'image': '0f3a5af0-8454-4441-a5f6-c53655b1b2b3.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Капуста брокколи с/м, перец болгарский, масло подсолнечное'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13284, 'combo': True, 'product': {'id': 617, 'name': 'Спагетти отварные 150 гр.', 'price': 69, 'carbohydrate': '35.74950', 'fat': '7.15650', 'fiber': '4.68000', 'energy': '226.12350', 'image': '66149542-2a5f-426e-9e58-bf327a581b76.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав Спагетти, масло подс.,соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13285, 'combo': False, 'product': {'id': 359, 'name': 'Лазанья грибная 200 гр.', 'price': 199, 'carbohydrate': '56.29400', 'fat': '14.49800', 'fiber': '19.03600', 'energy': '431.79400', 'image': 'f82d609c-7824-4492-b297-a0616726f9cb.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : грибы шампиньоны, лук репчатый, масло подсолнечное, паста для лазаньи, перец черный молотый, соль, сыр гауда, соус бешамель ( масло сливочное, молоко 3,2%, мускатный орех, мука пшеничная, соль, перец черный молотый.)'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13286, 'combo': False, 'product': {'id': 1218, 'name': 'Суп рисовый с куриными фрикадельками 250 гр.', 'price': 89, 'carbohydrate': '10.14000', 'fat': '4.60750', 'fiber': '6.47750', 'energy': '107.94000', 'image': 'dd6bbb7a-d17c-4725-b8b8-2da02e2012db.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав Бульон куриный, фрикадельки из куриного фарша,рис, морковь, лук репчатый,соль , перец'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13287, 'combo': False, 'product': {'id': 508, 'name': ' Картофельное пюре со шпинатом150 гр.', 'price': 89, 'carbohydrate': '26.91450', 'fat': '7.95750', 'fiber': '4.05450', 'energy': '195.50250', 'image': 'ee560f38-5b7b-41f8-8275-a4a2b3e7f8b1.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Картофель,молоко,масло сливочное,шпинат с/м.,соль'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13288, 'combo': False, 'product': {'id': 1642, 'name': 'Рис с укропом150 гр.', 'price': 69, 'carbohydrate': '47.23619', 'fat': '4.42347', 'fiber': '3.91797', 'energy': '241.06339', 'image': 'fb9a613c-3095-4a6b-a194-5a695b628b90.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Cостав:Рис,шпинат,масло раст.,специи'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13289, 'combo': False, 'product': {'id': 927, 'name': 'Салат "Столичный" с курицей 100 гр.', 'price': 89, 'carbohydrate': '5.98515', 'fat': '9.44750', 'fiber': '6.03912', 'energy': '133.12458', 'image': '298406ab-7fd7-4b54-8c47-ac94ea3ac828.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, морковь, филе куриное, огурцы маринованные, огурцы свежие, горошек консерв, яйцо куриное отварное, майонез, зелень, соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13290, 'combo': False, 'product': {'id': 947, 'name': 'Салат из крабовых палочек 100 гр.', 'price': 89, 'carbohydrate': '5.40000', 'fat': '9.16500', 'fiber': '2.91000', 'energy': '115.72500', 'image': '606430d1-cf3b-4d6d-ac82-050ed6bf6bd0.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Огурцы свежие, капуста пекинская, крабовые палочки,масйонез, кукуруза консервированная.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13291, 'combo': False, 'product': {'id': 992, 'name': 'Салат из томатов с редисом 100 гр.', 'price': 109, 'carbohydrate': '3.58000', 'fat': '5.16000', 'fiber': '0.80500', 'energy': '63.98000', 'image': '1c25edbd-0443-4865-a7e0-ba0c9417e44f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Помидоры свежие, редис, укроп, масло раст., соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13292, 'combo': True, 'product': {'id': 976, 'name': 'Салат из свежей капусты с зеленым горошком 100 гр.', 'price': 79, 'carbohydrate': '4.82248', 'fat': '7.27273', 'fiber': '2.26123', 'energy': '93.78938', 'image': '5f3ea239-a7b2-47e8-9de5-3ca456a6e175.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Капуста белокачанная, горошек консерв., зелень, масло раст., соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13293, 'combo': False, 'product': {'id': 958, 'name': 'Салат из огурцов с укропом 100 гр.', 'price': 89, 'carbohydrate': '2.87000', 'fat': '2.12600', 'fiber': '0.86200', 'energy': '34.06200', 'image': 'cc924895-5a6e-49d3-b344-13173340541a.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Cостав:Огурцы свежие, укроп,масло раст.,соль'}, 'category': {'id': 15, 'name': 'Салаты'}}]}}

    menu_items = dict_tests['menu']['items']
    to_create = []
    for menu_item in menu_items:
        try:
            if len(menu_item['product']['description']) < 3:
                menu_item['product']['description'] = 'Отсутствует'
        except TypeError:
            menu_item['product']['description'] = 'Отсутствует'

        if (len(Product.objects.filter(iditem=menu_item['product']['id'])) == 0) and (
                len([item for item in to_create if item.iditem == menu_item['product']['id']]) == 0):
            to_create.append(Product(
                iditem=menu_item['product']['id'],
                name=menu_item['product']['name'],
                price=menu_item['product']['price'],
                carbohydrate=menu_item['product']['carbohydrate'],
                fat=menu_item['product']['fat'],
                fiber=menu_item['product']['fiber'],
                energy=menu_item['product']['energy'],
                image=menu_item['product']['image'],
                vegan=menu_item['product']['vegan'],
                allergens=menu_item['product']['allergens'],
                lactose_free=menu_item['product']['lactose_free'],
                sugarless=menu_item['product']['sugarless'],
                gluten_free=menu_item['product']['gluten_free'],
                description=menu_item['product']['description'],
                category=menu_item['category']['name']
            ))
    Product.objects.bulk_create(to_create)


@transaction.atomic
def load_timetable(dict_tests):
    # Product.objects.all().delete()
    # dict_tests = {'menu': {'id': 682, 'date': '24.06.2022', 'status': 'completed', 'completed_at': '22.06.2022 17:52:31', 'created_at': '17.06.2022 10:26:17', 'combo_price': 350, 'location': {'id': 4, 'name': 'hadassah', 'subdomain': 'hadassah'}, 'items': [{'id': 13276, 'combo': False, 'product': {'id': 251, 'name': 'Говядина по-азиатски 75/75 гр.', 'price': 239, 'carbohydrate': '0.57539', 'fat': '11.42332', 'fiber': '21.60205', 'energy': '191.51808', 'image': 'a8faed5c-fd3e-40cf-bb93-6d86240a268e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: говядина, масло подсолнечное, соус соевый, крахмал, соус терияки, перец чили, масло кунжутное, кунжут, корень имбиря, перец болгарский, лук репчатый.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13277, 'combo': False, 'product': {'id': 337, 'name': 'Куриная ватрушка с грибным жульеном 120 гр.', 'price': 159, 'carbohydrate': '23.04720', 'fat': '17.42760', 'fiber': '20.17560', 'energy': '329.73120', 'image': '66366171-300e-469f-8692-de7da76785f4.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : Состав : фарш из курицы ( филе курицы, хлеб, соль, перекц , лук репчатый), масло подсолнечное, сыр Гауда, жульен грибной ( грибы шампиньоны, лук репчатый, масло подсолнечное, молоко 3,2%, сливки 33%, перец черный молотый, соль).'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13278, 'combo': False, 'product': {'id': 396, 'name': 'Перец фаршированный овощами, грибами и кус-кусом 200/50', 'price': 239, 'carbohydrate': '25.70250', 'fat': '8.97750', 'fiber': '4.95250', 'energy': '203.40750', 'image': '7bba3000-acb3-4b5d-aecd-aa0b7be477e5.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: перец болгарский, грибы шампиньоны, кускус, морковь, перец болгарский, томатный соус ( томатная паста, лук репчатый, морковь, перец черный молотый, соль, прованские травы),'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13279, 'combo': True, 'product': {'id': 1817, 'name': 'Суп-крем овощной 250 гр.', 'price': 99, 'carbohydrate': '21.50694', 'fat': '5.40708', 'fiber': '2.86319', 'energy': '146.14958', 'image': 'fb998852-3579-4a9a-bba7-abe5cccb8f32.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста брокколи, капуста цветная , лук репчатый, картофель, морковь, зхелень, сельдерей, перец, соль, масло оливковое, сливки 33 % .'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13280, 'combo': False, 'product': {'id': 1255, 'name': 'Тайский суп с лапшой и говядиной 250 гр.', 'price': 169, 'carbohydrate': '17.91500', 'fat': '14.48250', 'fiber': '15.07500', 'energy': '262.29000', 'image': '76113578-d361-41f9-9bad-31a37e26c856.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: шпинат, говядина, чеснок, имбирь, лук репчатый, морковь, масло подсолнечное, грибы шампиньоны, лапша гречневая, соевый соус, соль, перец.'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13281, 'combo': False, 'product': {'id': 434, 'name': 'Стейк из бедра индейки с томатной сальсой 100/50 гр.', 'price': 239, 'carbohydrate': '3.64950', 'fat': '16.14150', 'fiber': '21.92400', 'energy': '247.57050', 'image': 'df5fb311-1b7f-4373-bc4d-2ca869c8b3e7.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : филе индейки, соевый соус, тимьян, мед, масло подсолнечное, томатная сальса( помидор, лук репчатый, чеснок, кинза, соль, перец, масло оливковое).'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13282, 'combo': True, 'product': {'id': 446, 'name': 'Тефтели куриные с зеленым горошком в сметанном соусе 100/50гр.', 'price': 139, 'carbohydrate': '16.39800', 'fat': '12.20250', 'fiber': '14.38200', 'energy': '232.92450', 'image': '1b066181-48e5-4739-b847-6819afa21f54.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: фарш куриный (курица, соль, перец, лук, хлеб),горек зеленый, сметана, мука пшеничная, соль,перец черный молотый.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13283, 'combo': False, 'product': {'id': 514, 'name': 'Брокколи на пару с болгарским перцем 150 гр.', 'price': 119, 'carbohydrate': '7.41150', 'fat': '5.26650', 'fiber': '3.73650', 'energy': '91.98150', 'image': '0f3a5af0-8454-4441-a5f6-c53655b1b2b3.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Капуста брокколи с/м, перец болгарский, масло подсолнечное'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13284, 'combo': True, 'product': {'id': 617, 'name': 'Спагетти отварные 150 гр.', 'price': 69, 'carbohydrate': '35.74950', 'fat': '7.15650', 'fiber': '4.68000', 'energy': '226.12350', 'image': '66149542-2a5f-426e-9e58-bf327a581b76.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав Спагетти, масло подс.,соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13285, 'combo': False, 'product': {'id': 359, 'name': 'Лазанья грибная 200 гр.', 'price': 199, 'carbohydrate': '56.29400', 'fat': '14.49800', 'fiber': '19.03600', 'energy': '431.79400', 'image': 'f82d609c-7824-4492-b297-a0616726f9cb.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : грибы шампиньоны, лук репчатый, масло подсолнечное, паста для лазаньи, перец черный молотый, соль, сыр гауда, соус бешамель ( масло сливочное, молоко 3,2%, мускатный орех, мука пшеничная, соль, перец черный молотый.)'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13286, 'combo': False, 'product': {'id': 1218, 'name': 'Суп рисовый с куриными фрикадельками 250 гр.', 'price': 89, 'carbohydrate': '10.14000', 'fat': '4.60750', 'fiber': '6.47750', 'energy': '107.94000', 'image': 'dd6bbb7a-d17c-4725-b8b8-2da02e2012db.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав Бульон куриный, фрикадельки из куриного фарша,рис, морковь, лук репчатый,соль , перец'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13287, 'combo': False, 'product': {'id': 508, 'name': ' Картофельное пюре со шпинатом150 гр.', 'price': 89, 'carbohydrate': '26.91450', 'fat': '7.95750', 'fiber': '4.05450', 'energy': '195.50250', 'image': 'ee560f38-5b7b-41f8-8275-a4a2b3e7f8b1.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Картофель,молоко,масло сливочное,шпинат с/м.,соль'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13288, 'combo': False, 'product': {'id': 1642, 'name': 'Рис с укропом150 гр.', 'price': 69, 'carbohydrate': '47.23619', 'fat': '4.42347', 'fiber': '3.91797', 'energy': '241.06339', 'image': 'fb9a613c-3095-4a6b-a194-5a695b628b90.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Cостав:Рис,шпинат,масло раст.,специи'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13289, 'combo': False, 'product': {'id': 927, 'name': 'Салат "Столичный" с курицей 100 гр.', 'price': 89, 'carbohydrate': '5.98515', 'fat': '9.44750', 'fiber': '6.03912', 'energy': '133.12458', 'image': '298406ab-7fd7-4b54-8c47-ac94ea3ac828.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, морковь, филе куриное, огурцы маринованные, огурцы свежие, горошек консерв, яйцо куриное отварное, майонез, зелень, соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13290, 'combo': False, 'product': {'id': 947, 'name': 'Салат из крабовых палочек 100 гр.', 'price': 89, 'carbohydrate': '5.40000', 'fat': '9.16500', 'fiber': '2.91000', 'energy': '115.72500', 'image': '606430d1-cf3b-4d6d-ac82-050ed6bf6bd0.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Огурцы свежие, капуста пекинская, крабовые палочки,масйонез, кукуруза консервированная.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13291, 'combo': False, 'product': {'id': 992, 'name': 'Салат из томатов с редисом 100 гр.', 'price': 109, 'carbohydrate': '3.58000', 'fat': '5.16000', 'fiber': '0.80500', 'energy': '63.98000', 'image': '1c25edbd-0443-4865-a7e0-ba0c9417e44f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Помидоры свежие, редис, укроп, масло раст., соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13292, 'combo': True, 'product': {'id': 976, 'name': 'Салат из свежей капусты с зеленым горошком 100 гр.', 'price': 79, 'carbohydrate': '4.82248', 'fat': '7.27273', 'fiber': '2.26123', 'energy': '93.78938', 'image': '5f3ea239-a7b2-47e8-9de5-3ca456a6e175.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Капуста белокачанная, горошек консерв., зелень, масло раст., соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13293, 'combo': False, 'product': {'id': 958, 'name': 'Салат из огурцов с укропом 100 гр.', 'price': 89, 'carbohydrate': '2.87000', 'fat': '2.12600', 'fiber': '0.86200', 'energy': '34.06200', 'image': 'cc924895-5a6e-49d3-b344-13173340541a.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Cостав:Огурцы свежие, укроп,масло раст.,соль'}, 'category': {'id': 15, 'name': 'Салаты'}}]}}

    menu_items = dict_tests['menu']['items']
    to_create = []
    for menu_item in menu_items:
        menu_item_date = datetime.strptime(dict_tests['menu']['date'], "%d.%m.%Y").strftime("%Y-%m-%d")
        if len(Timetable.objects.filter(datetime=menu_item_date).filter(
                item=Product.objects.get(iditem=menu_item['product']['id']))) == 0:
            to_create.append(Timetable(
                datetime=menu_item_date,
                item=Product.objects.get(iditem=menu_item['product']['id'])
            ))
    Timetable.objects.bulk_create(to_create)


def index1(request):
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd',
                                              'vkd'),
                                          widgets={'ovd': CheckboxInput(
                                              attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'shd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'bd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'vbd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'nbd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'nkd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'vkd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'name': Textarea(attrs={'style': "display: none;"}),
                                              'description': Textarea(attrs={'style': "display: none;"}),
                                              'iditem': Textarea(attrs={'style': "display: none;"}),
                                              'category': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )
    queryset_salad = Product.objects.filter(category='Салаты')
    queryset_soup = Product.objects.filter(category='Первые блюда')
    if request.method == 'POST':
        formset_salad = ProductFormSet(request.POST, request.FILES, queryset=queryset_salad, prefix='salad')
        formset_soup = ProductFormSet(request.POST, request.FILES, queryset=queryset_soup, prefix='soup')
        if not formset_salad.is_valid() and not formset_soup.is_valid():
            return render(request, 'index1.html', {'formset_salad': formset_salad,
                                                   'formset_soup': formset_soup,
                                                   })
        else:
            formset_salad.save()
            formset_soup.save()
    else:
        formset_salad = ProductFormSet(queryset=queryset_salad, prefix='salad')
        formset_soup = ProductFormSet(queryset=queryset_soup, prefix='soup')
    return render(request, 'index1.html', {'formset_salad': formset_salad, 'formset_soup': formset_soup,
                                           })


@login_required
def index(request):
    # upload_file('daily_horoscopes/backup.json', 'test/backup.json', replace=False)

    error = ''
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd', 'vbd', 'nbd', 'nkd',
                                              'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category'),
                                          widgets={'ovd': CheckboxInput(
                                              attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'ovd_sugarless': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'shd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'bd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'vbd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'nbd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'nkd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'vkd': CheckboxInput(
                                                  attrs={'class': 'form-check-input', 'type': 'checkbox'}),
                                              'name': Textarea(attrs={'style': "display: none;"}),
                                              'description': Textarea(attrs={'style': "display: none;"}),
                                              'carbohydrate': Textarea(attrs={'style': "display: none;"}),
                                              'iditem': Textarea(attrs={'style': "display: none;"}),
                                              'fat': Textarea(attrs={'style': "display: none;"}),
                                              'fiber': Textarea(attrs={'style': "display: none;"}),
                                              'energy': Textarea(attrs={'style': "display: none;"}),
                                              'category': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )
    if request.method == 'GET':
        date_default = str(date.today())
    else:
        date_default = str(request.POST['datetime'])

    queryset_salad = Product.objects.filter(timetable__datetime=date_default).filter(category='Салаты')
    queryset_soup = Product.objects.filter(timetable__datetime=date_default).filter(category='Первые блюда')
    queryset_main_dishes = Product.objects.filter(timetable__datetime=date_default).filter(category='Вторые блюда')
    queryset_side_dishes = Product.objects.filter(timetable__datetime=date_default).filter(category='Гарниры')
    if request.method == 'POST' and 'save' in request.POST:
        formset_salad = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset_salad, prefix='salad')
        formset_soup = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset_soup, prefix='soup')
        formset_main_dishes = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset_main_dishes, prefix='main_dishes')
        formset_side_dishes = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset_side_dishes, prefix='side_dishes')

        if not formset_salad.is_valid() \
                or not formset_soup.is_valid() \
                or not formset_main_dishes.is_valid() \
                or not formset_side_dishes.is_valid():
            return render(request,
                          'index.html',
                          {'formset_salad': formset_salad,
                           'formset_soup': formset_soup,
                           'formset_main_dishes': formset_main_dishes,
                           'formset_side_dishes': formset_side_dishes,
                           })
        else:
            formset_salad.save()
            formset_soup.save()
            formset_main_dishes.save()
            formset_side_dishes.save()
            date_default = str(request.POST['datetime'])
            queryset_salad = Product.objects.filter(timetable__datetime=date_default).filter(category='Салаты')
            queryset_soup = Product.objects.filter(timetable__datetime=date_default).filter(category='Первые блюда')
            queryset_main_dishes = Product.objects.filter(timetable__datetime=date_default).filter(
                category='Вторые блюда')
            queryset_side_dishes = Product.objects.filter(timetable__datetime=date_default).filter(category='Гарниры')

    if request.method == 'POST' and 'find_date' in request.POST:
        form_date = TimetableForm(request.POST)
        if form_date.is_valid():

            queryset_salad = Product.objects.filter(timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(
                category='Салаты')
            queryset_soup = Product.objects.filter(timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(
                category='Первые блюда')
            queryset_main_dishes = Product.objects.filter(
                timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(
                category='Вторые блюда')
            queryset_side_dishes = Product.objects.filter(
                timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(category='Гарниры')

            date_default = str(form_date.cleaned_data["datetime"])
            formset_salad = ProductFormSet(queryset=queryset_salad, prefix='salad')
            formset_soup = ProductFormSet(queryset=queryset_soup, prefix='soup')
            formset_main_dishes = ProductFormSet(queryset=queryset_main_dishes, prefix='main_dishes')
            formset_side_dishes = ProductFormSet(queryset=queryset_side_dishes, prefix='side_dishes')
            data = {
                'form_date': form_date,
                'error': error,
                'formset_salad': formset_salad,
                'formset_main_dishes': formset_main_dishes,
                'formset_side_dishes': formset_side_dishes,
                'formset_soup': formset_soup,
                # 'formset_e': formset._errors,
            }
            return render(request, 'index.html', context=data)
        else:
            error = 'Некорректные данные'
    else:
        formset_salad = ProductFormSet(queryset=queryset_salad, prefix='salad')
        formset_soup = ProductFormSet(queryset=queryset_soup, prefix='soup')
        formset_main_dishes = ProductFormSet(queryset=queryset_main_dishes, prefix='main_dishes')
        formset_side_dishes = ProductFormSet(queryset=queryset_side_dishes, prefix='side_dishes')

        form_date = TimetableForm(initial={'datetime': date_default})
        data = {
            'form_date': form_date,
            'error': error,
            'formset_salad': formset_salad,
            'formset_main_dishes': formset_main_dishes,
            'formset_side_dishes': formset_side_dishes,
            'formset_soup': formset_soup,
            # 'formset_e': formset._errors
        }
    return render(request, 'index.html', context=data)


class BaseAPIView(APIView):
    def post(self, request):
        data = request.data
        data_str = str(data)
        data_dict = dict(data)
        # data_dict = {'menu': {'id': 703, 'date': '01.07.2022', 'status': 'completed', 'completed_at': '30.06.2022 10:55:08', 'created_at': '27.06.2022 11:01:57', 'combo_price': 350, 'location': {'id': 4, 'name': 'hadassah', 'subdomain': 'hadassah'}, 'items': [{'id': 13787, 'combo': False, 'product': {'id': 984, 'name': 'Салат из свежей моркови с сельдереем с оливковым маслом 100 гр.', 'price': 69, 'carbohydrate': '7.46851', 'fat': '5.15697', 'fiber': '0.92781', 'energy': '79.99800', 'image': '08577f99-4797-43e1-a85b-ee8da0e6dd84.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13788, 'combo': False, 'product': {'id': 237, 'name': 'Биточки картофельные с луком и грибами 200 гр. ', 'price': 159, 'carbohydrate': '50.58400', 'fat': '11.60000', 'fiber': '8.03400', 'energy': '338.86000', 'image': 'b0eb83a1-fd20-432c-ac23-fb6a64eae743.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель шампиньоны, сухари панировочные, мука пшеничная, масло подсолнечное, перец черный молотый, соль.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13789, 'combo': False, 'product': {'id': 261, 'name': 'Горбуша в слоеном тесте 120 гр.', 'price': 199, 'carbohydrate': '22.70400', 'fat': '26.44320', 'fiber': '21.53040', 'energy': '414.92280', 'image': '0e7abcb0-3d74-46a5-8853-712e09deb374.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : горбуша филе, масло подсолнечное, соль, перец, шпинат, лимон сок, яйцо, вода, тесто слоеное.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13790, 'combo': True, 'product': {'id': 344, 'name': 'Куриное бедрышко по-грузински150 гр.', 'price': 159, 'carbohydrate': '0.20250', 'fat': '19.12800', 'fiber': '38.91450', 'energy': '328.62450', 'image': '4caa3d15-11bf-4107-a009-97e041e2db8a.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : курица бедро на кости, масло подсолнечное, соль, перец черный молотый, соус Аджика, соус Ткемали.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13791, 'combo': False, 'product': {'id': 313, 'name': 'Кесадилья с курицей и овощами 260 гр', 'price': 279, 'carbohydrate': '39.96200', 'fat': '17.21980', 'fiber': '23.97720', 'energy': '410.73500', 'image': '772aa424-e2c8-4880-bbb7-99a94bb3f59e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: тортилья пшеничная, сыр моцарелла, грибы шампиньоны,куриное филе, перец болгарский, лук репчатый, лук зеленый, соус терияки , масло подсолнечное, соль, перец черный молотый, морковь, чеснок, помидоры.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13792, 'combo': False, 'product': {'id': 425, 'name': 'Рулетик из индейки с кабачком и базиликом 100гр.', 'price': 189, 'carbohydrate': '1.31400', 'fat': '6.46600', 'fiber': '16.15800', 'energy': '128.08200', 'image': 'e1481c14-784b-4a16-964f-de4fa75ce9cd.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: филе индейки, кабачки/цукини, масло подсолнечное, соль, перец черный молотый, базилик.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13793, 'combo': False, 'product': {'id': 345, 'name': 'Куриное филе в сливочно-шпинатном соусе с грибами 70/50 гр.', 'price': 179, 'carbohydrate': '2.49360', 'fat': '17.94120', 'fiber': '13.53480', 'energy': '221.54880', 'image': '9e3e0f22-54af-46cb-991f-4035f55cfa6e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : куриное филе, перец черный молотый, соль, масло подсолнечное, соус из шпината( масло подсолнечное, соль, перец, мука пшеничная, шпинат, сливки 33%), грибы шампиньоны, лук репчатый.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13794, 'combo': False, 'product': {'id': 621, 'name': 'Тыква запеченная с морковью 150 гр.', 'price': 99, 'carbohydrate': '12.49950', 'fat': '0.40050', 'fiber': '1.80000', 'energy': '60.79950', 'image': '167335b3-bf49-4448-be6e-9b43292fea88.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: тыква, морковь, мед, соевый соус, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13795, 'combo': False, 'product': {'id': 626, 'name': 'Фасоль стручковая на пару 150 гр.', 'price': 99, 'carbohydrate': '6.24030', 'fat': '8.84430', 'fiber': '3.80060', 'energy': '119.76540', 'image': '581bd457-e289-4248-a84b-352612f3fb4a.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав : фасоль стручковая, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13796, 'combo': True, 'product': {'id': 631, 'name': 'Фузили отварные 150 гр.', 'price': 69, 'carbohydrate': '52.27500', 'fat': '7.36200', 'fiber': '7.02000', 'energy': '303.43800', 'image': 'ff52060f-3da0-4e9e-aecf-f17ca766c299.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: макароны, соль, масло подсолнечное. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13797, 'combo': False, 'product': {'id': 1029, 'name': 'Салат слоеный с курицей 120 гр.', 'price': 149, 'carbohydrate': '10.05600', 'fat': '26.34360', 'fiber': '11.49360', 'energy': '323.29320', 'image': 'b156c6d4-c245-4ea3-b781-f9331c2acd37.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: куриное филе, чернослив, яйцо отварное, сыр " Гауда", лук репчатый, орехи грецкие, огурцы свежие, майонез, соль, зелень, гранат.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13798, 'combo': False, 'product': {'id': 1172, 'name': 'Гаспаччо 250 гр.', 'price': 129, 'carbohydrate': '6.43250', 'fat': '7.08750', 'fiber': '1.34000', 'energy': '94.87250', 'image': 'ddae15cc-d56c-4242-9219-c17f08de7c02.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13799, 'combo': False, 'product': {'id': 198, 'name': 'Стейк из семги с соусом "Шафран" 100/50 гр', 'price': 399, 'carbohydrate': '68.48620', 'fat': '11.00240', 'fiber': '19.90020', 'energy': '452.57230', 'image': '4982a970-fad8-4b9c-8d2c-2a3b0fb27923.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Филе семги, рис басмати, сливки, лук репчатый,уксус винный, куркума,сок лимона,соль, перец.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13800, 'combo': True, 'product': {'id': 1269, 'name': 'Щи из свежей капусты с опятами 250 гр.', 'price': 99, 'carbohydrate': '10.32000', 'fat': '3.35250', 'fiber': '2.48750', 'energy': '81.40000', 'image': 'bdbf0e45-8716-4842-8f93-060f0b2e1f34.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: капуста б/к, лук репчатый, морковь, картофель, чеснок, паста томатная, зелень, сахар, соль, перец, масло подсолнеч, лавровый лист, зелень, помидоры, грибы опята.'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13801, 'combo': False, 'product': {'id': 239, 'name': 'Бифштекс рубленый с луком 100/20 гр.', 'price': 189, 'carbohydrate': '5.30160', 'fat': '21.83400', 'fiber': '19.57920', 'energy': '296.03040', 'image': '3fa0e7de-6439-4e23-8fcd-c5da52d36f99.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: говядина, молоко 3,2%, соль, перец, масло подсолнечное, лук репчатый, мука пшеничная, масло подсолнечное, фарш куриный.'}, 'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13802, 'combo': False, 'product': {'id': 1194, 'name': 'Суп с красной чечевицой и тыквой 250 гр.', 'price': 89, 'carbohydrate': '21.55750', 'fat': '16.58250', 'fiber': '2.88250', 'energy': '247.01500', 'image': 'cd767c65-00bf-4848-bd87-5e993f5e97ec.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: морковь, лук репчатый, чеснок, чечевица красная, кумин, паприка, перец красный острый, масло оливковое, зелень, тыква, соль.'}, 'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13803, 'combo': False, 'product': {'id': 553, 'name': 'Картофель бэби с паприкой 150 гр.', 'price': 79, 'carbohydrate': '32.96250', 'fat': '2.62500', 'fiber': '3.33900', 'energy': '168.83250', 'image': 'f50daab0-a320-4fdf-a575-6235a76a0f60.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель мини, масло подсолнечное, соль, перец черный молотый, паприка.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13804, 'combo': True, 'product': {'id': 926, 'name': 'Салат "Провансаль" 100 гр.', 'price': 79, 'carbohydrate': '5.64604', 'fat': '8.42506', 'fiber': '1.34201', 'energy': '103.77877', 'image': '2860a33e-8077-4895-b959-484e9d9b3f93.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: морковь, капуста б/к, яблоки, клюква, сахарный песок, масло подсолнечное, уксус, чеснок, соль.'}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13805, 'combo': False, 'product': {'id': 2071, 'name': 'Салат картофельный по-турецки 150 гр', 'price': 79, 'carbohydrate': '22.07097', 'fat': '7.58601', 'fiber': '2.93720', 'energy': '168.31272', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13806, 'combo': False, 'product': {'id': 966, 'name': 'Салат из печеной груши , айсберга и сыра фета 120 гр.', 'price': 149, 'carbohydrate': '4.22640', 'fat': '18.90240', 'fiber': '2.47560', 'energy': '196.93080', 'image': '43748b37-ec02-4607-879c-1b17324e4c3b.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: груша , сыр " Сиртаки", айсберг , лимон сок, масло подсолнечное, соль, куриное филе.'}, 'category': {'id': 15, 'name': 'Салаты'}}]}}
        load_menu(data_dict)
        load_timetable(data_dict)
        Base.objects.create(base=data_str)
        return Response(data)


#
# def register(request):
#     """ Регистрация нового пользователя"""
#     errors = []
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # делаем запрос на регистрацию нового пользователя (DRF)
#             url = 'https://intense-badlands-65950.herokuapp.com/api/v1/auth/users/'
#             headers = {'content-type': 'application/json'}
#             payload = {
#                 'email': user_form.cleaned_data['email'],
#                 'username': user_form.cleaned_data['username'],
#                 'password': user_form.cleaned_data['password'],
#             }
#             response = requests.post(url, headers=headers, json=payload).json()
#
#             if payload['username'] == response.get(
#                     'username'):  # если имя пользователя есть в ответе регестрация прошла успешно
#                 return render(request, 'registration/register_done.html', {'new_user': user_form.cleaned_data})
#             else:
#                 errors = list(response.values())
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'registration/register.html', {'user_form': user_form, 'errors': errors})
#
#
# def get_token(username, password):
#     response = {
#         'token': None,
#         'error': None
#     }
#     url = 'https://intense-badlands-65950.herokuapp.com/auth/token/login/'
#     headers = {'content-type': 'application/json'}
#     payload = {
#         'username': username,
#         'password': password,
#
#     }
#     response_on_json = requests.post(url, headers=headers, json=payload)
#     response_on_python = response_on_json.json()
#     if response_on_python.get("auth_token"):
#         if len(response_on_python["auth_token"]) != 40:
#             response['error'] = response_on_python["auth_token"]
#         else:
#             response['token'] = response_on_python["auth_token"]
#     return response
#
#
def user_login(request):
    errors = None
    if request.method == 'POST':
        user_form = UserloginForm(request.POST)
        user = authenticate(username=user_form.data['username'],
                            password=user_form.data['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            errors = 'Пользователя с таким именем и паролем не существует'
    else:
        user_form = UserloginForm()
    return render(request, 'registration/login.html', {'user_form': user_form,
                                                       'errors': errors})
#
#
# def profile(request):
#     return render(
#         request=request,
#         template_name='profile.html',
#         context=context
#     )
