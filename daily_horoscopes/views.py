from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Base, Product, Timetable
from .forms import UserRegistrationForm, UserloginForm, TimetableForm
from django.forms import modelformset_factory
from .serializers import ProductSerializer
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import calendar, datetime
from datetime import datetime
from datetime import date
from django.template import RequestContext
from django.core.paginator import Paginator

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
def load_menu(dict_tests, dict_tk):
    menu_items = dict_tests['menu']['items']
    to_create = []
    for menu_item in menu_items:
        try:
            if len(menu_item['product']['description']) < 3:
                menu_item['product']['description'] = 'Отсутствует'
        except TypeError:
            menu_item['product']['description'] = 'Отсутствует'
        key = dict_tk.get(menu_item['product']['name'])
        if key == None:
            key = "Отсутствует"


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
                category=menu_item['category']['name'],
                cooking_method=key
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


@login_required
def index(request):
    # js = open("daily_horoscopes/descriptions_from_tk.json").read()
    # dict_tk_descriptions = json.loads(js)
    # all = Product.objects.all()
    # for item in all:
    #     value = dict_tk_descriptions.get(item.name)
    #     if value == None:
    #         continue
    #     item.description = value
    error = ''
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd',
                                              'vbd', 'nbd', 'nkd',
                                              'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category',
                                              'cooking_method'),
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
                                              'cooking_method': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )
    if request.method == 'GET':
        date_default = str(date.today())
    else:
        date_default = str(request.POST['datetime'])
    count_prosucts = len(Product.objects.all())
    count_prosucts_labeled = len(Product.objects.filter(
        Q(ovd='True') | Q(ovd_sugarless='True') | Q(shd='True') | Q(bd='True') | Q(vbd='True') | Q(nbd='True') | Q(
            nkd='True') | Q(vkd='True')))
    count_prosucts_not_labeled = count_prosucts - count_prosucts_labeled
    progress = int(count_prosucts_labeled * 100 / count_prosucts)
    queryset_salad = Product.objects.filter(timetable__datetime=date_default).filter(category='Салаты')
    queryset_soup = Product.objects.filter(timetable__datetime=date_default).filter(category='Первые блюда')
    queryset_main_dishes = Product.objects.filter(timetable__datetime=date_default).filter(category='Вторые блюда')
    queryset_side_dishes = Product.objects.filter(timetable__datetime=date_default).filter(category='Гарниры')
    if request.method == 'POST' and 'save' in request.POST:
        form_date = TimetableForm(request.POST)
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
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'form_date': form_date,
                           'progress': progress,
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
            date_default = str(form_date.cleaned_data["datetime"])
            queryset_salad = Product.objects.filter(timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(
                category='Салаты')
            queryset_soup = Product.objects.filter(timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(
                category='Первые блюда')
            queryset_main_dishes = Product.objects.filter(
                timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(
                category='Вторые блюда')
            queryset_side_dishes = Product.objects.filter(
                timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(category='Гарниры')

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
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,

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
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,

            # 'formset_e': formset._errors
        }
    return render(request, 'index.html', context=data)



# @login_required
# def catalog(request):
#     error = ''
#     ProductFormSet = modelformset_factory(Product,
#                                           fields=(
#                                               'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd',
#                                               'vbd', 'nbd', 'nkd',
#                                               'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category',
#                                               'cooking_method'),
#                                           widgets={'ovd': CheckboxInput(
#                                               attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'ovd_sugarless': CheckboxInput(
#                                                   attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'shd': CheckboxInput(
#                                                   attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'bd': CheckboxInput(
#                                                   attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'vbd': CheckboxInput(
#                                                   attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'nbd': CheckboxInput(
#                                                   attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'nkd': CheckboxInput(
#                                                   attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'vkd': CheckboxInput(
#                                                   attrs={'class': 'form-check-input', 'type': 'checkbox'}),
#                                               'name': Textarea(attrs={'style': "display: none;"}),
#                                               'description': Textarea(attrs={'style': "display: none;"}),
#                                               'carbohydrate': Textarea(attrs={'style': "display: none;"}),
#                                               'iditem': Textarea(attrs={'style': "display: none;"}),
#                                               'fat': Textarea(attrs={'style': "display: none;"}),
#                                               'fiber': Textarea(attrs={'style': "display: none;"}),
#                                               'energy': Textarea(attrs={'style': "display: none;"}),
#                                               'category': Textarea(attrs={'style': "display: none;"}),
#                                               'cooking_method': Textarea(attrs={'style': "display: none;"}),
#                                           },
#                                           extra=0, )
#     count_prosucts = len(Product.objects.all())
#     count_prosucts_labeled = len(Product.objects.filter(
#         Q(ovd='True') | Q(ovd_sugarless='True') | Q(shd='True') | Q(bd='True') | Q(vbd='True') | Q(nbd='True') | Q(
#             nkd='True') | Q(vkd='True')))
#     count_prosucts_not_labeled = count_prosucts - count_prosucts_labeled
#
#     queryset = Product.objects.all()
#     queryset = Paginator(queryset, 5)
#     if request.method == 'POST' and 'save' in request.POST:
#         formset = \
#             ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='all')
#         if not formset.is_valid():
#             return render(request,
#                           'catalog.html',
#                           {'formset': formset,
#                            'count_prosucts': count_prosucts,
#                            'count_prosucts_labeled': count_prosucts_labeled,
#                            'count_prosucts_not_labeled': count_prosucts_not_labeled,
#
#                            })
#         else:
#             formset.save()
#             data = {
#                 'formset': formset,
#                 'count_prosucts': count_prosucts,
#                 'count_prosucts_labeled': count_prosucts_labeled,
#                 'count_prosucts_not_labeled': count_prosucts_not_labeled,
#                 # 'formset_e': formset._errors
#             }
#             return render(request, 'catalog.html', context=data)
#
#     else:
#         formset = ProductFormSet(queryset=queryset, prefix='all')
#
#         data = {
#             'formset': formset,
#             'count_prosucts': count_prosucts,
#             'count_prosucts_labeled': count_prosucts_labeled,
#             'count_prosucts_not_labeled': count_prosucts_not_labeled,
#             # 'formset_e': formset._errors
#         }
#     return render(request, 'catalog.html', context=data)

def page_func(page):
    if page == '50':
        page_start = 0
        page_fin = 49
    if page == '100':
        page_start = 50
        page_fin = 99
    if page == '150':
        page_start = 100
        page_fin = 149
    if page == '200':
        page_start = 150
        page_fin = 199
    if page == '250':
        page_start = 200
        page_fin = 249
    if page == '300':
        page_start = 250
        page_fin = 299
    if page == '350':
        page_start = 300
        page_fin = 335
    return page_start, page_fin

def get_stat(category):
    count_prosucts = len(Product.objects.filter(category=category))
    count_prosucts_labeled = len(Product.objects.filter(category=category).filter(
        Q(ovd='True') | Q(ovd_sugarless='True') | Q(shd='True') | Q(bd='True') | Q(vbd='True') | Q(nbd='True') | Q(
            nkd='True') | Q(vkd='True')))
    count_prosucts_not_labeled = count_prosucts - count_prosucts_labeled
    progress = int(count_prosucts_labeled * 100 / count_prosucts)
    return count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress


@login_required
def catalog_salad(request, page):
    # 213
    error = ''
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd',
                                              'vbd', 'nbd', 'nkd',
                                              'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category',
                                              'cooking_method'),
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
                                              'cooking_method': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Салаты')

    page_start, page_finish = page_func(page)
    q = Product.objects.filter(category='Салаты')[page_start:page_finish]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])



    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='salad')
        if not formset.is_valid():
            return render(request,
                          'salad.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,
                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Салаты')
            data = {
                'page': page,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
                # 'formset_e': formset._errors
            }
            return render(request, 'salad.html', context=data)

    else:
        formset = ProductFormSet(queryset=queryset, prefix='salad')

        data = {
            'page': page,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
            # 'formset_e': formset._errors
        }
    return render(request, 'salad.html', context=data)

@login_required
def catalog_soup(request, page):
    # 134
    error = ''
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd',
                                              'vbd', 'nbd', 'nkd',
                                              'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category',
                                              'cooking_method'),
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
                                              'cooking_method': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Первые блюда')

    page_start, page_finish = page_func(page)
    q = Product.objects.filter(category='Первые блюда')[page_start:page_finish]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])



    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='soup')
        if not formset.is_valid():
            return render(request,
                          'soup.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,

                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Первые блюда')
            data = {
                'page': page,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
                # 'formset_e': formset._errors
            }
            return render(request, 'soup.html', context=data)

    else:
        formset = ProductFormSet(queryset=queryset, prefix='soup')

        data = {
            'page': page,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
            # 'formset_e': formset._errors
        }
    return render(request, 'soup.html', context=data)


@login_required
def catalog_main_dishes(request, page):
    # 335
    error = ''
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd',
                                              'vbd', 'nbd', 'nkd',
                                              'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category',
                                              'cooking_method'),
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
                                              'cooking_method': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Вторые блюда')

    page_start, page_finish = page_func(page)
    q = Product.objects.filter(category='Вторые блюда')[page_start:page_finish]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])



    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='main_dishes')
        if not formset.is_valid():
            return render(request,
                          'main_dishes.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,

                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Вторые блюда')
            data = {
                'page': page,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
                # 'formset_e': formset._errors
            }
            return render(request, 'main_dishes.html', context=data)

    else:
        formset = ProductFormSet(queryset=queryset, prefix='main_dishes')

        data = {
            'page': page,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
            # 'formset_e': formset._errors
        }
    return render(request, 'main_dishes.html', context=data)

@login_required
def catalog_side_dishes(request, page):
    # 157
    error = ''
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'ovd_sugarless', 'shd', 'bd',
                                              'vbd', 'nbd', 'nkd',
                                              'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category',
                                              'cooking_method'),
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
                                              'cooking_method': Textarea(attrs={'style': "display: none;"}),
                                          },
                                          extra=0, )
    count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Гарниры')

    page_start, page_finish = page_func(page)
    q = Product.objects.filter(category='Гарниры')[page_start:page_finish]
    queryset = Product.objects.filter(id__in=[item_q.id for item_q in q])



    if request.method == 'POST' and 'save' in request.POST:
        formset = \
            ProductFormSet(request.POST, request.FILES, queryset=queryset, prefix='side_dishes')
        if not formset.is_valid():
            return render(request,
                          'side_dishes.html',
                          {'formset': formset,
                           'count_prosucts': count_prosucts,
                           'count_prosucts_labeled': count_prosucts_labeled,
                           'count_prosucts_not_labeled': count_prosucts_not_labeled,
                           'progress': progress,

                           })
        else:
            formset.save()
            count_prosucts, count_prosucts_labeled, count_prosucts_not_labeled, progress = get_stat('Гарниры')
            data = {
                'page': page,
                'formset': formset,
                'count_prosucts': count_prosucts,
                'count_prosucts_labeled': count_prosucts_labeled,
                'count_prosucts_not_labeled': count_prosucts_not_labeled,
                'progress': progress,
                # 'formset_e': formset._errors
            }
            return render(request, 'side_dishes.html', context=data)

    else:
        formset = ProductFormSet(queryset=queryset, prefix='side_dishes')

        data = {
            'page': page,
            'formset': formset,
            'count_prosucts': count_prosucts,
            'count_prosucts_labeled': count_prosucts_labeled,
            'count_prosucts_not_labeled': count_prosucts_not_labeled,
            'progress': progress,
            # 'formset_e': formset._errors
        }
    return render(request, 'side_dishes.html', context=data)


class BaseAPIView(APIView):
    def post(self, request):
        data = request.data
        data_str = str(data)
        data_dict = dict(data)
        # data_dict = {'menu': {'id': 723, 'date': '05.06.2022', 'status': 'completed', 'completed_at': '07.07.2022 12:30:43', 'created_at': '07.07.2022 12:30:43', 'combo_price': 350, 'location': {'id': 4, 'name': 'hadassah', 'subdomain': 'hadassah'}, 'items': [{'id': 15007, 'combo': False, 'product': {'id': 624, 'name': 'Фасоль красная в томатном соусе 150 гр.', 'price': 109, 'carbohydrate': '40.04100', 'fat': '1.89750', 'fiber': '12.04950', 'energy': '225.43350', 'image': 'df2337f2-8975-4d0c-bf3e-202de140fff2.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: фасоль красная, соль, томатный соус ( лук репчатый, морковь, томатная паста, сельдерей, прованский травы, сахар песок, соль, перец черный молотый).'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15008, 'combo': False, 'product': {'id': 522, 'name': 'Булгур с овощами 100 г', 'price': 49, 'carbohydrate': '51.51700', 'fat': '5.82100', 'fiber': '10.31200', 'energy': '299.70700', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15009, 'combo': False, 'product': {'id': 575, 'name': 'Пенне с маслом 150 гр.', 'price': 69, 'carbohydrate': '52.27500', 'fat': '7.36200', 'fiber': '7.02000', 'energy': '303.43800', 'image': '9f8d7fcf-43a1-43a4-92a7-bc722d2d33cd.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: макароны пенне, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15010, 'combo': False, 'product': {'id': 587, 'name': 'Рагу овощное с тыквой 150 гр.', 'price': 99, 'carbohydrate': '13.78490', 'fat': '13.73242', 'fiber': '2.14578', 'energy': '187.31904', 'image': 'd1578992-f0ed-44a0-93b6-cb95eb82d967.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: капуста б/к, капуста брокколи,тыква , лук репчатый, масло подсолнечное, морковь, перец болгарский, помидоры, чеснок, зелень, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15011, 'combo': False, 'product': {'id': 579, 'name': 'Пенне с томатным соусом 100/20г', 'price': 49, 'carbohydrate': '36.68040', 'fat': '5.66760', 'fiber': '4.83960', 'energy': '217.08600', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15012, 'combo': False, 'product': {'id': 577, 'name': 'Пенне с соусом песто 150 гр.', 'price': 79, 'carbohydrate': '49.10100', 'fat': '8.67150', 'fiber': '6.03750', 'energy': '298.60350', 'image': 'a3cc4a1f-e2ef-4705-b834-48148d4a4b5e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Пенне отварные, соус Песто(базилик,орех кедр.,чеснок,масло раст.,соль)'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15013, 'combo': False, 'product': {'id': 581, 'name': 'Перловка с овощами 100гр.', 'price': 49, 'carbohydrate': '20.56600', 'fat': '4.96900', 'fiber': '2.42900', 'energy': '136.69700', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15014, 'combo': False, 'product': {'id': 536, 'name': 'Гречка отварная 100гр.', 'price': 39, 'carbohydrate': '21.52800', 'fat': '4.99700', 'fiber': '3.93100', 'energy': '146.80700', 'image': '438a8d54-9bcc-4afc-8096-52ba96200b2b.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15015, 'combo': False, 'product': {'id': 1465, 'name': '_Рис припущенный с кедровыми орехами 150гр.', 'price': 0, 'carbohydrate': '51.48150', 'fat': '5.07000', 'fiber': '3.73800', 'energy': '266.50950', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15016, 'combo': False, 'product': {'id': 619, 'name': 'Спагетти с томатным соусом 100/20г', 'price': 69, 'carbohydrate': '34.00500', 'fat': '1.13100', 'fiber': '4.37100', 'energy': '163.68300', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15017, 'combo': False, 'product': {'id': 538, 'name': 'Гречка с грибами 100 гр.', 'price': 59, 'carbohydrate': '22.25111', 'fat': '2.73686', 'fiber': '4.53494', 'energy': '131.77598', 'image': '85a8574b-4725-4d4d-812b-4d2c1597b54c.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15018, 'combo': False, 'product': {'id': 520, 'name': 'Булгур с кабачками 100гр.', 'price': 49, 'carbohydrate': '50.37328', 'fat': '4.48240', 'fiber': '10.71857', 'energy': '328.64618', 'image': '83d7da4c-cdd3-4d15-a789-cf362ddce93e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15019, 'combo': False, 'product': {'id': 567, 'name': 'Кус-Кус с болгарским перцем 100гр.', 'price': 59, 'carbohydrate': '22.23800', 'fat': '0.13500', 'fiber': '3.58200', 'energy': '104.49800', 'image': '9a70fdd1-93aa-4eb9-ab07-65cb9777de9b.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15020, 'combo': False, 'product': {'id': 1477, 'name': '-Картофель по-деревенски 150 гр.', 'price': 0, 'carbohydrate': '27.15000', 'fat': '0.60000', 'fiber': '3.00000', 'energy': '126.00000', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15021, 'combo': False, 'product': {'id': 609, 'name': 'Рис с овощами и карри 100г.', 'price': 49, 'carbohydrate': '31.58500', 'fat': '1.60100', 'fiber': '2.37100', 'energy': '150.23000', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15022, 'combo': False, 'product': {'id': 607, 'name': 'Рис с овощами 100г.', 'price': 49, 'carbohydrate': '31.58500', 'fat': '1.60100', 'fiber': '2.37100', 'energy': '150.23000', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15023, 'combo': False, 'product': {'id': 591, 'name': 'Рис микс 100 гр', 'price': 59, 'carbohydrate': '36.88800', 'fat': '4.74900', 'fiber': '2.93000', 'energy': '202.01600', 'image': '3c64ec16-1012-493f-b4e9-258a6eb0c004.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15024, 'combo': False, 'product': {'id': 593, 'name': 'Рис микс с овощами 100 гр', 'price': 59, 'carbohydrate': '31.70586', 'fat': '5.37882', 'fiber': '2.56139', 'energy': '185.47844', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15025, 'combo': False, 'product': {'id': 613, 'name': 'Рис со шпинатом 100гр.', 'price': 49, 'carbohydrate': '31.49079', 'fat': '2.94898', 'fiber': '2.61198', 'energy': '160.70893', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15026, 'combo': False, 'product': {'id': 526, 'name': 'Гарнир из зеленой гречки с кунжутом 100гр.', 'price': 59, 'carbohydrate': '24.04568', 'fat': '7.38990', 'fiber': '5.06493', 'energy': '182.95256', 'image': '348f4270-6338-4178-8a5e-4beb9dd6cb91.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15027, 'combo': False, 'product': {'id': 601, 'name': 'Рис с зеленым горошком 100г.', 'price': 49, 'carbohydrate': '32.23800', 'fat': '0.25800', 'fiber': '2.47200', 'energy': '141.16100', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15028, 'combo': False, 'product': {'id': 1838, 'name': 'Картофельная ватрушка с грибами 120', 'price': 99, 'carbohydrate': '15.04440', 'fat': '5.15160', 'fiber': '3.61200', 'energy': '120.99720', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15029, 'combo': False, 'product': {'id': 589, 'name': 'Рис "Басмати" 150 гр.', 'price': 89, 'carbohydrate': '118.35000', 'fat': '1.05000', 'fiber': '10.05000', 'energy': '523.05000', 'image': '0689155d-4139-40d9-8e08-4edea92d5242.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис Басмати, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15030, 'combo': False, 'product': {'id': 528, 'name': 'Гарнир из зеленой гречки с овощами 100гр.', 'price': 59, 'carbohydrate': '23.50884', 'fat': '5.09797', 'fiber': '4.72397', 'energy': '158.81194', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15031, 'combo': False, 'product': {'id': 530, 'name': 'Гарнир из зеленой гречки с тыквенными семечками 100гр.', 'price': 59, 'carbohydrate': '23.17085', 'fat': '5.08097', 'fiber': '4.64997', 'energy': '157.01395', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15032, 'combo': False, 'product': {'id': 614, 'name': 'Рис со шпинатом 150 гр.', 'price': 69, 'carbohydrate': '42.10800', 'fat': '4.38900', 'fiber': '3.52650', 'energy': '218.67450', 'image': '6f408292-db3d-46c7-924e-dd3cd0a39e92.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Cостав:Рис,шпинат,масло раст.,специи'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15033, 'combo': False, 'product': {'id': 576, 'name': 'Пенне с соусом песто 100г.', 'price': 59, 'carbohydrate': '32.73400', 'fat': '5.78100', 'fiber': '4.02500', 'energy': '199.06900', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15034, 'combo': False, 'product': {'id': 600, 'name': 'Рис с горошком и кукурузой 100 гр', 'price': 49, 'carbohydrate': '32.13912', 'fat': '3.57355', 'fiber': '2.59939', 'energy': '171.11597', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15035, 'combo': False, 'product': {'id': 603, 'name': 'Рис с карри 100гр.', 'price': 49, 'carbohydrate': '35.50513', 'fat': '0.23556', 'fiber': '2.71397', 'energy': '155.00150', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15036, 'combo': False, 'product': {'id': 569, 'name': 'Кус-Кус с овощами 100 гр.', 'price': 59, 'carbohydrate': '19.97400', 'fat': '1.23700', 'fiber': '3.13500', 'energy': '103.56500', 'image': 'b12d4511-3b96-4e42-8b8d-cc2a8f26a655.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15037, 'combo': False, 'product': {'id': 635, 'name': 'Фузили с сыром 150 гр.', 'price': 79, 'carbohydrate': '47.34750', 'fat': '8.00850', 'fiber': '9.06150', 'energy': '297.70800', 'image': '6435873d-0845-4ccd-93b7-aad11a0eeaf4.jpg', 'vegan': None, 'allergens': 1, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: макароны фузили, сыр "Гауда", соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15038, 'combo': False, 'product': {'id': 616, 'name': 'Спагетти отварные 100 гр.', 'price': 39, 'carbohydrate': '23.83300', 'fat': '4.77100', 'fiber': '3.12000', 'energy': '150.74900', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15039, 'combo': False, 'product': {'id': 611, 'name': 'Рис с паприкой 100гр.', 'price': 49, 'carbohydrate': '35.76083', 'fat': '0.25771', 'fiber': '2.78746', 'energy': '156.51351', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15040, 'combo': False, 'product': {'id': 634, 'name': 'Фузили с сыром 100г.', 'price': 59, 'carbohydrate': '31.56500', 'fat': '5.33900', 'fiber': '6.04100', 'energy': '198.47200', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': None}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15041, 'combo': False, 'product': {'id': 1859, 'name': 'Капуста брюссельская в сливочном соус 150 гр.', 'price': 129, 'carbohydrate': '0.00000', 'fat': '0.00000', 'fiber': '0.00000', 'energy': '0.00000', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста брюссельская, соус сливочный( сливки 33%, уксус винный, перец черный молотый, зелень, сок лимона, лук репчатый).'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15042, 'combo': False, 'product': {'id': 1885, 'name': 'Дикий рис с овощами 150 гр.', 'price': 250, 'carbohydrate': '47.55150', 'fat': '8.06700', 'fiber': '3.84150', 'energy': '278.17500', 'image': '0601bcfb-6509-46fe-9afd-45846b0b6110.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15043, 'combo': False, 'product': {'id': 514, 'name': 'Брокколи на пару с болгарским перцем 150 гр.', 'price': 129, 'carbohydrate': '7.41150', 'fat': '5.26650', 'fiber': '3.73650', 'energy': '91.98150', 'image': '0f3a5af0-8454-4441-a5f6-c53655b1b2b3.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Капуста брокколи с/м, перец болгарский, масло подсолнечное'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15044, 'combo': False, 'product': {'id': 505, 'name': ' Картофельное пюре с кунжутным маслом 150 гр.', 'price': 79, 'carbohydrate': '22.97550', 'fat': '9.39600', 'fiber': '2.85750', 'energy': '187.89600', 'image': 'a1c28e26-5d7a-4559-8d16-3b8d80bd084c.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, молоко, масло сливочное, соль, кунжутно масло.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15045, 'combo': False, 'product': {'id': 513, 'name': 'Брокколи на пару с болг. перцем и соусом Терияки 150 гр.', 'price': 129, 'carbohydrate': '8.32772', 'fat': '5.35236', 'fiber': '4.28759', 'energy': '98.63245', 'image': 'a0d911e5-920b-4bd8-88a5-6eb97dcff88b.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: брокколи, масло подсолнечное, соль, соус Терияки. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15046, 'combo': False, 'product': {'id': 518, 'name': 'Булгур отварной с оливковым маслом 150 гр.', 'price': 69, 'carbohydrate': '86.40000', 'fat': '1.95000', 'fiber': '18.45000', 'energy': '513.00000', 'image': '9d495b3a-6df1-4cb4-9d4d-142b85a2187b.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: брокколи, масло оливковое, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15047, 'combo': False, 'product': {'id': 521, 'name': 'Булгур с кабачками 150 гр.', 'price': 69, 'carbohydrate': '75.55992', 'fat': '6.72360', 'fiber': '16.07786', 'energy': '492.96926', 'image': '76439412-05c6-47de-861c-1c00d323a0d3.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Булгур ,кабачки,масло оливковое.,специи'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15048, 'combo': False, 'product': {'id': 529, 'name': 'Гарнир из зеленой гречки с овощами 150 гр.', 'price': 89, 'carbohydrate': '35.26350', 'fat': '7.64700', 'fiber': '7.08600', 'energy': '238.21950', 'image': '67304843-e434-4c71-b9dc-ff4f118e3eab.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: гречка зеленая, лук репчатый, помидоры, зелень, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15049, 'combo': False, 'product': {'id': 531, 'name': 'Гарнир из зеленой гречки с тыквенными семечками 150 гр.', 'price': 89, 'carbohydrate': '34.75627', 'fat': '7.62145', 'fiber': '6.97495', 'energy': '235.52093', 'image': '24bfe73d-072f-41d5-847c-6864a6cad682.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: зеленая гречка, лук репчатый, семечки тыквенные, зелень , соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15050, 'combo': False, 'product': {'id': 532, 'name': 'Гратен из цветной капусты 150 гр.', 'price': 139, 'carbohydrate': '4.78050', 'fat': '7.86000', 'fiber': '9.41550', 'energy': '127.51950', 'image': 'b6e3d312-1656-4f22-8eec-a6d3311de9e6.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста цветная, масло подсолнечное, соус Бешамель(мука,масло слив.,молоко,мускатный орех,соль, перец).'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15051, 'combo': False, 'product': {'id': 574, 'name': 'Овощная смесь на пару 150 гр.', 'price': 129, 'carbohydrate': '4.87890', 'fat': '4.79341', 'fiber': '11.87554', 'energy': '110.15696', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Говяжья вырезка, грибы белые, лук ,карри, соль, перец черный молотый, капуста цветная, кольраби, фасоль стручковая,морковь, перец болгарский, масло оливковое.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15052, 'combo': False, 'product': {'id': 519, 'name': 'Булгур по-восточному 150 гр.', 'price': 89, 'carbohydrate': '0.00000', 'fat': '0.00000', 'fiber': '0.00000', 'energy': '0.00000', 'image': '7830ba64-c55e-485c-8beb-64e2b4555504.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: булгур, соль, томатная паста, морковь, лук репчатый, бульон куриный, мята, масло сливочное, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15053, 'combo': False, 'product': {'id': 580, 'name': 'Пенне с томатным соусом 120/30 гр.', 'price': 69, 'carbohydrate': '44.56650', 'fat': '7.02900', 'fiber': '5.85450', 'energy': '264.94050', 'image': '01658ca3-d801-4b0a-baa6-22b1dc51a0b5.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: макароны отварные, томатный соус ( морковь, лук репчатый , сельдерей, томатная паста, соль, перец черный молотый, прованские травы, сахар песоск).'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15054, 'combo': False, 'product': {'id': 582, 'name': 'Перловка с овощами 150 гр.', 'price': 69, 'carbohydrate': '30.84900', 'fat': '7.45350', 'fiber': '3.64350', 'energy': '205.04550', 'image': 'cb3b3a68-f202-41d1-9be4-e185d505a646.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : крупа перловая, морковь, лук репчатый, масло подсолнечное, соль, зелень в асс.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15055, 'combo': False, 'product': {'id': 583, 'name': 'Плов с нутом и курагой 150 гр.', 'price': 79, 'carbohydrate': '47.85817', 'fat': '9.12861', 'fiber': '6.42406', 'energy': '299.28784', 'image': 'cb8f9770-f61c-4740-88a9-98c60a0971f9.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Рис,морковь,лук,нут, курага,чеснок,кумин,специи,масло раст.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15056, 'combo': False, 'product': {'id': 592, 'name': 'Рис микс 150 гр.', 'price': 89, 'carbohydrate': '55.33200', 'fat': '7.12350', 'fiber': '4.39500', 'energy': '303.02400', 'image': '1730acd8-226a-4284-a94f-05d81c781c3b.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: рис отварной, рис дикий, соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15057, 'combo': False, 'product': {'id': 594, 'name': 'Рис микс с овощами 150 гр.', 'price': 109, 'carbohydrate': '47.55879', 'fat': '8.06824', 'fiber': '3.84209', 'energy': '278.21765', 'image': 'd4cc6858-b8cc-4277-b6d7-e9c9cb6bd28e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной,рис дикий, морковь, перец болгарский, кабачки , соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15058, 'combo': False, 'product': {'id': 595, 'name': 'Рис отварной с кукурузой 150 гр.', 'price': 69, 'carbohydrate': '48.35700', 'fat': '0.38700', 'fiber': '3.70800', 'energy': '211.74150', 'image': 'dc4d3757-5080-41f5-8912-c7efdbf0dda8.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной, кукуруза, соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15059, 'combo': False, 'product': {'id': 590, 'name': 'Рис Басмати с кедровыми орехами 150 гр.', 'price': 119, 'carbohydrate': '51.48150', 'fat': '5.07000', 'fiber': '3.73800', 'energy': '266.50950', 'image': 'f7582238-1498-4080-ae71-c75fb862a704.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис Басмати, соль, орехи кедровые, масл подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15060, 'combo': False, 'product': {'id': 596, 'name': 'Рис припущенный 150 гр.', 'price': 59, 'carbohydrate': '53.25750', 'fat': '0.35400', 'fiber': '4.07100', 'energy': '232.50150', 'image': 'e5eb62e5-9926-4a44-82f5-2ab7984913a3.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: рис отварной, соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15061, 'combo': False, 'product': {'id': 599, 'name': 'Рис с вермишелью по-восточному 150 гр.', 'price': 79, 'carbohydrate': '117.32850', 'fat': '1.09500', 'fiber': '10.46100', 'energy': '521.00550', 'image': '4b346fe0-2072-48b1-9fbf-69c17f589205.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис круглозерный, макароны из твердых сортов пшеницы, куриный бульон (вода питьевая, лавровый лист, морковь, соль, перец, курица), масло сливочное, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15062, 'combo': False, 'product': {'id': 602, 'name': 'Рис с зеленым горошком 150 гр.', 'price': 79, 'carbohydrate': '48.35700', 'fat': '0.38700', 'fiber': '3.70800', 'energy': '211.74150', 'image': '3502aa6d-be2c-4640-a068-9712fcbfa2a5.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: рис отварной, зеленый горошек, соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15063, 'combo': False, 'product': {'id': 597, 'name': 'Рис припущенный с кедровыми орехами 150 гр.', 'price': 89, 'carbohydrate': '51.48150', 'fat': '5.07000', 'fiber': '3.73800', 'energy': '266.50950', 'image': '94928247-cb34-43b0-94ab-b5acc7720419.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной,кедровые орехи , соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15064, 'combo': False, 'product': {'id': 604, 'name': 'Рис с карри 150 гр.', 'price': 59, 'carbohydrate': '53.25770', 'fat': '0.35334', 'fiber': '4.07096', 'energy': '232.50225', 'image': '30e158be-ae70-45a7-b9f8-59f9f5d2ab6d.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: рис, масло подсолнечное, карри, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15065, 'combo': False, 'product': {'id': 605, 'name': 'Рис с куркумой 150 гр.', 'price': 59, 'carbohydrate': '51.92550', 'fat': '6.55650', 'fiber': '3.62850', 'energy': '281.22450', 'image': '63965214-d0ce-45c7-ac53-20a43cdcb3fb.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: рис отварной, куркума, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15066, 'combo': False, 'product': {'id': 610, 'name': 'Рис с овощами и карри 150 гр.', 'price': 69, 'carbohydrate': '47.37750', 'fat': '2.40150', 'fiber': '3.55650', 'energy': '225.34500', 'image': '01a8f99c-3d22-42cb-a356-9208cfa398ce.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной, морковь, лук репчатый, кукуруза, горошек зеленый, масло подсолнечное, соль, карри.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15067, 'combo': False, 'product': {'id': 615, 'name': 'Рис со шпинатом и кукурузой 150 гр.', 'price': 69, 'carbohydrate': '48.35700', 'fat': '0.38700', 'fiber': '3.70800', 'energy': '211.74150', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Cостав: рис,шпинат, кукуруза , масло раст.,специи.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15068, 'combo': False, 'product': {'id': 608, 'name': 'Рис с овощами и стручковой фасолью 150 гр.', 'price': 89, 'carbohydrate': '41.57214', 'fat': '2.45689', 'fiber': '4.11143', 'energy': '204.84325', 'image': '5bec8b2d-ca23-4727-a617-b4af127b4892.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной, морковь, лук репчатый, кукуруза, горошек зеленый, масло подсолнечное, соль, стручковая фасоль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15069, 'combo': False, 'product': {'id': 617, 'name': 'Спагетти отварные 150 гр.', 'price': 69, 'carbohydrate': '35.74950', 'fat': '7.15650', 'fiber': '4.68000', 'energy': '226.12350', 'image': '66149542-2a5f-426e-9e58-bf327a581b76.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав Спагетти, масло подс.,соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15070, 'combo': False, 'product': {'id': 618, 'name': 'Спагетти с кабачками и соусом чили 120/30 гр.', 'price': 79, 'carbohydrate': '39.30025', 'fat': '0.48980', 'fiber': '5.14445', 'energy': '182.18855', 'image': '6342e4ea-32a7-4e96-b150-9ef2f0b66172.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: спагетти, кабачки, соус чили сладкий.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15071, 'combo': False, 'product': {'id': 620, 'name': 'Спагетти с томатным соусом 120/30 гр.', 'price': 69, 'carbohydrate': '34.00500', 'fat': '1.13100', 'fiber': '4.37100', 'energy': '163.68300', 'image': 'c0387c33-dc46-4ef5-b6ed-68999ea6053c.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: спагетти, томатный соус ( лук репчатый, морковь, томатная паста, сельдерей, прованский травы, сахар песок, соль, перец черный молотый).'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15072, 'combo': False, 'product': {'id': 621, 'name': 'Тыква запеченная с морковью 150 гр.', 'price': 99, 'carbohydrate': '12.49950', 'fat': '0.40050', 'fiber': '1.80000', 'energy': '60.79950', 'image': '167335b3-bf49-4448-be6e-9b43292fea88.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: тыква, морковь, мед, соевый соус, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15073, 'combo': False, 'product': {'id': 622, 'name': 'Тыква запеченная с яблоком и медом 150 гр.', 'price': 119, 'carbohydrate': '12.60000', 'fat': '0.49950', 'fiber': '1.50000', 'energy': '60.90000', 'image': 'f3ab6270-84eb-42cf-bac2-92384996064f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: тыква, яблоко, мед, кунжут, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15074, 'combo': False, 'product': {'id': 625, 'name': 'Фасоль стручковая в томатном соусе 150 гр.', 'price': 109, 'carbohydrate': '6.59266', 'fat': '0.28086', 'fiber': '3.34465', 'energy': '42.27245', 'image': 'd278e15c-a93d-405d-8d97-c7ba5cf68a88.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав:Фасоль стручковая,помидоры, базилик сушенный, масло раст.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15075, 'combo': False, 'product': {'id': 626, 'name': 'Фасоль стручковая на пару 150 гр.', 'price': 99, 'carbohydrate': '6.24030', 'fat': '8.84430', 'fiber': '3.80060', 'energy': '119.76540', 'image': '581bd457-e289-4248-a84b-352612f3fb4a.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав : фасоль стручковая, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15076, 'combo': False, 'product': {'id': 627, 'name': 'Фасоль стручковая с болгарским перцем 150 гр.', 'price': 119, 'carbohydrate': '6.71250', 'fat': '7.76400', 'fiber': '3.71250', 'energy': '111.57900', 'image': '8703f974-4a0d-42e8-85d5-7244c13043f0.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: фасоль стручковая, перец болгарский, кунжут, зелень, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15077, 'combo': False, 'product': {'id': 628, 'name': 'Фасоль стручковая с миндалем 150 гр.', 'price': 109, 'carbohydrate': '6.03900', 'fat': '8.55900', 'fiber': '3.67800', 'energy': '115.90200', 'image': 'ae6236c5-145d-4bb1-a8dc-1c4163ecf05e.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: фасоль стручковая, миндаль, лук репчатый, масло подсолнечое, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15078, 'combo': False, 'product': {'id': 629, 'name': 'Фасоль стручковая с яйцом 150 гр.', 'price': 109, 'carbohydrate': '4.96050', 'fat': '13.13850', 'fiber': '7.67550', 'energy': '168.79500', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Фасоль стручковая, яйцо куриное , соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15079, 'combo': False, 'product': {'id': 631, 'name': 'Фузили отварные 150 гр.', 'price': 69, 'carbohydrate': '52.27500', 'fat': '7.36200', 'fiber': '7.02000', 'energy': '303.43800', 'image': 'ff52060f-3da0-4e9e-aecf-f17ca766c299.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: макароны, соль, масло подсолнечное. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15080, 'combo': False, 'product': {'id': 630, 'name': 'Фетучини 150 гр.', 'price': 109, 'carbohydrate': '22.16640', 'fat': '20.29560', 'fiber': '7.84320', 'energy': '302.70240', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15081, 'combo': False, 'product': {'id': 632, 'name': 'Фузили с овощами 150 гр.', 'price': 79, 'carbohydrate': '44.25150', 'fat': '11.62350', 'fiber': '5.66550', 'energy': '304.27950', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: макароны фузили, кабачки, морковь, перец болгарский, зелень, перец черный молотый, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15082, 'combo': False, 'product': {'id': 633, 'name': 'Фузили с соусом песто 150 гр.', 'price': 79, 'carbohydrate': '49.10100', 'fat': '8.67150', 'fiber': '6.03750', 'energy': '298.60350', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Пенне отварные, соус Песто(базилик,орех кедр.,чеснок,масло раст.,соль)'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15083, 'combo': False, 'product': {'id': 636, 'name': 'Цветная капуста гриль 150 гр.', 'price': 109, 'carbohydrate': '7.19100', 'fat': '8.97750', 'fiber': '2.90700', 'energy': '121.18500', 'image': 'a943112a-b63e-4739-b111-e19af0fb71b5.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: цветная капуста, масло подсолнечное, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15084, 'combo': False, 'product': {'id': 640, 'name': 'Цветная капуста с яйцом 150 гр.', 'price': 129, 'carbohydrate': '5.85000', 'fat': '3.81000', 'fiber': '6.21000', 'energy': '82.53000', 'image': '0e08c7d6-4e41-48cb-a527-d8fcea7c84d3.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: цветная капуста, яйцо куриное, масло подсолнечное, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15085, 'combo': False, 'product': {'id': 641, 'name': 'Чечевица в томатном соусе 150 гр.', 'price': 79, 'carbohydrate': '39.77550', 'fat': '1.75950', 'fiber': '13.65750', 'energy': '229.57200', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : чечевица, томатный соус( лук репчатый, морковь, перец черный молотый, соль, прованские травы, сахар песок, соль).'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15086, 'combo': False, 'product': {'id': 642, 'name': 'Чечевица отварная с кунжутными семечками 150 гр.', 'price': 79, 'carbohydrate': '45.58350', 'fat': '2.92650', 'fiber': '16.82700', 'energy': '275.98650', 'image': 'c18196a5-f269-4392-84e3-309ffd39cbb6.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: чечевица, кунжут, масло кунжутное, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15087, 'combo': False, 'product': {'id': 643, 'name': 'Чечевица с томатами 150 гр.', 'price': 79, 'carbohydrate': '33.98669', 'fat': '11.26088', 'fiber': '11.79204', 'energy': '284.45381', 'image': 'cde4f33c-8cb7-47cd-a0b8-fba429eeb068.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: чечевица, чеснок, зелень, помидоры, лук репчатый, соль, перец черный молотый. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15088, 'combo': False, 'product': {'id': 556, 'name': 'Картофель жареный с грибами 150 гр.', 'price': 89, 'carbohydrate': '33.67950', 'fat': '2.47800', 'fiber': '4.05750', 'energy': '173.25450', 'image': '26c201b0-e7a5-4708-b871-243e3bc7f303.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Картофель, грибы шампиньоны, лук репчатый, масло раст., специи'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15089, 'combo': False, 'product': {'id': 1639, 'name': 'Картофель жареный с луком 150 гр.', 'price': 89, 'carbohydrate': '33.67950', 'fat': '2.47800', 'fiber': '4.05750', 'energy': '173.25450', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель , лук репчатый белый, масло подсолнечное, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15090, 'combo': False, 'product': {'id': 557, 'name': 'Картофель запеченный с вешенками 150 гр.', 'price': 99, 'carbohydrate': '26.30250', 'fat': '2.27700', 'fiber': '3.35250', 'energy': '139.11150', 'image': 'bc48fd0a-db7b-4966-8c3d-215a0abba2e1.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: картофель, вешенки грибы, лук репчатый, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15091, 'combo': False, 'product': {'id': 1640, 'name': 'Картофель тушеный с овощами 150 гр.', 'price': 99, 'carbohydrate': '33.70500', 'fat': '2.92950', 'fiber': '3.43950', 'energy': '174.94050', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, лук репчатый, масло подсолнечное, морковь, перец болгарский, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15092, 'combo': False, 'product': {'id': 1515, 'name': 'Микс паровых овощей 150 гр.', 'price': 109, 'carbohydrate': '6.99591', 'fat': '8.05039', 'fiber': '3.54295', 'energy': '114.61347', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15093, 'combo': False, 'product': {'id': 598, 'name': 'Рис с болгарским перцем 150 гр.', 'price': 79, 'carbohydrate': '48.74250', 'fat': '5.04750', 'fiber': '3.66600', 'energy': '255.06450', 'image': 'b84f65f4-7680-4064-a30a-1ef573e8ec4a.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной, перец болгарский, соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15094, 'combo': False, 'product': {'id': 506, 'name': ' Картофельное пюре с сельдереем 150 гр.', 'price': 89, 'carbohydrate': '26.06602', 'fat': '7.80535', 'fiber': '3.85577', 'energy': '189.94146', 'image': 'd55dd6f9-aeaa-4a44-a9b2-0a2d6773b209.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, молоко 3,2% , масло сливочное, соль, корень сельдерея.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15095, 'combo': False, 'product': {'id': 507, 'name': ' Картофельное пюре с тыквой 150 гр.', 'price': 79, 'carbohydrate': '26.46000', 'fat': '7.81650', 'fiber': '3.86100', 'energy': '191.62800', 'image': '569699ce-3e53-4220-90b3-b4f0077c3b7c.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, молоко 3,2% , масло сливочное, соль,тыква.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15096, 'combo': False, 'product': {'id': 515, 'name': 'Брокколи на пару с кунжутным маслом 150 гр.', 'price': 119, 'carbohydrate': '7.19852', 'fat': '4.38157', 'fiber': '3.92717', 'energy': '83.93375', 'image': 'c60690a1-751b-4c6f-896b-98e4434aba43.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: брокколи, соль, масло кунжутное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15097, 'combo': False, 'product': {'id': 516, 'name': 'Брокколи на пару с соусом Терияки 150 гр.', 'price': 119, 'carbohydrate': '8.31900', 'fat': '5.41800', 'fiber': '4.54050', 'energy': '100.19850', 'image': 'd74c1cb4-2e96-44d6-8310-fa8502a4a7c8.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: брокколи, масло подсолнечное, соль, соус Терияки.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15098, 'combo': False, 'product': {'id': 517, 'name': 'Булгур отварной 150 гр.', 'price': 59, 'carbohydrate': '86.40000', 'fat': '1.95000', 'fiber': '18.45000', 'energy': '513.00000', 'image': '36118cd6-b2cd-445b-a097-75e9c7ff6db6.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: булгур, масло подсолнечное,соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15099, 'combo': False, 'product': {'id': 1638, 'name': 'Булгур с грибами 150 гр.', 'price': 79, 'carbohydrate': '33.39150', 'fat': '3.10800', 'fiber': '6.80550', 'energy': '188.76450', 'image': '65bf1efe-6d19-490a-bd1e-6349ecb847ae.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: булгур , грибы шампиньоны, лук репчатый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15100, 'combo': False, 'product': {'id': 523, 'name': 'Булгур с овощами 150 гр.', 'price': 79, 'carbohydrate': '77.27550', 'fat': '8.73150', 'fiber': '15.46800', 'energy': '449.56050', 'image': 'a2415ee1-1748-4856-9d2d-ccb9c203ae3d.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: булгур, соль, масло подсолнечное, лук репчатый, зелень.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15101, 'combo': False, 'product': {'id': 524, 'name': 'Булгур с тыквой 250 гр.', 'price': 89, 'carbohydrate': '96.02500', 'fat': '6.71750', 'fiber': '19.07250', 'energy': '520.83500', 'image': '7f1e92d3-1850-4cbb-8fbb-0c4272ef565e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: тыква, булгур, масло подсолнечное, '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15102, 'combo': False, 'product': {'id': 525, 'name': 'Гарнир из зеленой гречки с вялеными томатами 150 гр.', 'price': 109, 'carbohydrate': '37.50880', 'fat': '4.49480', 'fiber': '7.39330', 'energy': '220.05820', 'image': '630775a1-ea88-4d29-961e-abd6b8927d06.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: гречка, соль, лук репчатый, зелень, масло подсолнечное, орехи кедровые, томаты вяленные.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15103, 'combo': False, 'product': {'id': 527, 'name': 'Гарнир из зеленой гречки с кунжутом 150 гр.', 'price': 89, 'carbohydrate': '36.06852', 'fat': '11.08485', 'fiber': '7.59740', 'energy': '274.42884', 'image': 'c51e04c8-6851-4ce0-a996-bf900732dce5.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: зеленая гречка, соль, перец, масло подсолнечное, кунжут, зелень.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15104, 'combo': False, 'product': {'id': 546, 'name': 'Капуста тушеная 150 гр.', 'price': 99, 'carbohydrate': '11.97113', 'fat': '10.70035', 'fiber': '2.49805', 'energy': '154.17991', 'image': 'ee2c3ac4-7a05-4298-9ccb-ebdf39e4101f.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Капуста б/к, морковь,лук репчатый,томатная паста, масло раст.,соль,сахар, перец черный молотый'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15105, 'combo': False, 'product': {'id': 803, 'name': 'Драники картофельные 100 гр', 'price': 89, 'carbohydrate': '18.74040', 'fat': '4.40040', 'fiber': '2.55960', 'energy': '124.80000', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: соль, перец черный молотый, мука пшеничная, масло подсолнечное, картофель, сметана 20%.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15106, 'combo': False, 'product': {'id': 806, 'name': 'Морковные биточки 100/20гр.', 'price': 89, 'carbohydrate': '13.64040', 'fat': '4.28520', 'fiber': '1.99560', 'energy': '101.10480', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: морковь, крупа манная, масл оподсолнечное, соль, сухари панировочные.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15107, 'combo': False, 'product': {'id': 807, 'name': 'Оладьи кабачково-овсяные 100 гр.', 'price': 139, 'carbohydrate': '7.73377', 'fat': '6.19912', 'fiber': '2.28273', 'energy': '95.85808', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: хлопья овсяные, цукини, сметана 20 %, яйцо куриное, масло подсолнечное, мука пшеничная, соль, зелень.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15108, 'combo': False, 'product': {'id': 558, 'name': 'Картофель запеченный с карри 150 гр.', 'price': 89, 'carbohydrate': '27.15000', 'fat': '0.60000', 'fiber': '3.00000', 'energy': '126.00000', 'image': '465c4a87-cd6e-46b2-92f8-eafeb8a341eb.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: картофель, карри, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15109, 'combo': False, 'product': {'id': 545, 'name': 'Капуста карри с льняными семечками 150 гр.', 'price': 89, 'carbohydrate': '6.81450', 'fat': '5.28450', 'fiber': '2.61000', 'energy': '85.26450', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста б/к, карри, масло подсолнечное, соль, перец черный молотый, семена льна.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15110, 'combo': False, 'product': {'id': 568, 'name': 'Кус-Кус с болгарским перцем 150 гр.', 'price': 109, 'carbohydrate': '33.35700', 'fat': '0.20250', 'fiber': '5.37300', 'energy': '156.74700', 'image': '2c964a1c-7de2-46bd-ad98-7b37007ca4d1.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав : кускус, перец болгарский, соль , масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15111, 'combo': False, 'product': {'id': 571, 'name': 'Мясо по-восточному (жаркое) 250 гр.', 'price': 239, 'carbohydrate': '24.64005', 'fat': '15.47003', 'fiber': '10.07002', 'energy': '278.06809', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:говядина, картофель, лук репчатый, масло подсолнечное, орегано, парика, перец болгарский, перец черный молотый, соль, томатная паста, помидоры.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15112, 'combo': False, 'product': {'id': 573, 'name': 'Овощи припущенные 150 гр.', 'price': 129, 'carbohydrate': '6.99781', 'fat': '8.05258', 'fiber': '3.54392', 'energy': '114.64460', 'image': '73413e45-7e01-41fc-a907-dc135dfe586c.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: капуста брокколи, капуста цветная, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15113, 'combo': False, 'product': {'id': 606, 'name': 'Рис с куркумой и зеленным горошком 150 гр.', 'price': 69, 'carbohydrate': '48.80100', 'fat': '3.09150', 'fiber': '3.42450', 'energy': '236.71950', 'image': '8a0efb8c-ad1a-489c-b1f4-06069ec58d5a.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной, куркума, зеленый горошек, соль, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15114, 'combo': False, 'product': {'id': 612, 'name': 'Рис с паприкой 150 гр.', 'price': 59, 'carbohydrate': '53.64124', 'fat': '0.38656', 'fiber': '4.18119', 'energy': '234.77027', 'image': '35322538-5673-43fc-bc56-b99ca4ae7a7e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис отварной, паприка , масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15115, 'combo': False, 'product': {'id': 637, 'name': 'Цветная капуста на пару с кунжутным маслом 150 гр.', 'price': 129, 'carbohydrate': '7.19100', 'fat': '4.23150', 'fiber': '2.90700', 'energy': '78.48000', 'image': 'aa42c6e2-5612-404c-97f0-4479e4a43645.jpg', 'vegan': 1, 'allergens': 1, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: капуста цветная, масло кунжутное, специи.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15116, 'combo': False, 'product': {'id': 638, 'name': 'Цветная капуста на пару со сливочным маслом 150 гр.', 'price': 119, 'carbohydrate': '7.23150', 'fat': '4.35450', 'fiber': '2.93100', 'energy': '79.84350', 'image': '9e9997c3-818d-4d46-b294-53b63debfb7b.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: цветная капуста, маслосливочное, соль, перец черный молотый. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15117, 'combo': False, 'product': {'id': 639, 'name': 'Цветная капуста с морковью 150 гр.', 'price': 89, 'carbohydrate': '10.68750', 'fat': '0.42750', 'fiber': '2.67900', 'energy': '57.31650', 'image': '728ed3b8-acaa-4914-a345-5b94bdd66d00.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15118, 'combo': False, 'product': {'id': 508, 'name': ' Картофельное пюре со шпинатом150 гр.', 'price': 89, 'carbohydrate': '26.91450', 'fat': '7.95750', 'fiber': '4.05450', 'energy': '195.50250', 'image': 'ee560f38-5b7b-41f8-8275-a4a2b3e7f8b1.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Картофель,молоко,масло сливочное,шпинат с/м.,соль'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15119, 'combo': False, 'product': {'id': 512, 'name': 'Брокколи на пару 150 гр.', 'price': 129, 'carbohydrate': '6.91500', 'fat': '4.20900', 'fiber': '3.77250', 'energy': '80.62800', 'image': 'ebc37f04-41cb-4fe9-921e-a1adae4c2db0.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: брокколи, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15120, 'combo': False, 'product': {'id': 1637, 'name': 'Брокколи с сыром 150 гр.', 'price': 119, 'carbohydrate': '6.89882', 'fat': '4.19915', 'fiber': '3.76367', 'energy': '80.43935', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: брокколи, масло подсолнечное, соль, сыр Гауда.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15121, 'combo': False, 'product': {'id': 504, 'name': ' Картофельное пюре 150 гр.', 'price': 89, 'carbohydrate': '22.97550', 'fat': '7.14750', 'fiber': '2.85750', 'energy': '167.66400', 'image': '31a0906c-99f6-4d68-964d-bc9b40615fde.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, молоко, масло сливочное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15122, 'combo': False, 'product': {'id': 541, 'name': 'Гречка с овощами 150 гр.', 'price': 69, 'carbohydrate': '42.76050', 'fat': '8.65500', 'fiber': '7.27950', 'energy': '278.05050', 'image': 'e3f556ac-0eac-4031-92f0-8e80240aad7b.jpg', 'vegan': 1, 'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: гречка отварная , лук репчатый, морковь, зелень, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15123, 'combo': False, 'product': {'id': 542, 'name': 'Запеканка из цветной капусты 150 гр.', 'price': 139, 'carbohydrate': '4.78050', 'fat': '7.86000', 'fiber': '9.41550', 'energy': '127.51950', 'image': '05fe74f1-9cff-447e-bba0-5e7ef177f52f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста цветная, сыр моцарелла, тимьян, соль, перец черный молотый, масло одсолнечное, яйцо куриное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15124, 'combo': False, 'product': {'id': 533, 'name': 'Гречка зеленая отварная 150 гр.', 'price': 79, 'carbohydrate': '37.99220', 'fat': '11.67605', 'fiber': '8.00260', 'energy': '289.06524', 'image': 'c615c6e7-7659-4850-9c47-8a481d98e919.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: гречка зеленая, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15125, 'combo': False, 'product': {'id': 534, 'name': 'Гречка отварная с с кунжутными семечками 150 гр.', 'price': 69, 'carbohydrate': '32.90250', 'fat': '8.49450', 'fiber': '6.76950', 'energy': '235.14300', 'image': 'fb605c63-e51e-4389-a343-65b9b5d78908.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: гречка, кунжутные семечки, соль, масло оливковое.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15126, 'combo': False, 'product': {'id': 539, 'name': 'Гречка с грибами 150 гр.', 'price': 89, 'carbohydrate': '33.39150', 'fat': '3.10800', 'fiber': '6.80550', 'energy': '188.76450', 'image': '379af4a6-f45e-4865-87af-074ba0ece3c2.jpg', 'vegan': 1, 'allergens': 1, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: гречка, соль, грибы шампиньоны.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15127, 'combo': False, 'product': {'id': 535, 'name': 'Гречка отварная с оливковым маслом и тыквенными семечками 150гр.', 'price': 79, 'carbohydrate': '32.29200', 'fat': '6.79050', 'fiber': '5.89650', 'energy': '213.86550', 'image': '658493d2-0208-447e-8cf1-c99a4d5e4923.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: гречка, тыквенные семечки, соль, масло оливковое.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15128, 'combo': False, 'product': {'id': 548, 'name': 'Картофель бэби отварной с зеленью 150 гр.', 'price': 79, 'carbohydrate': '32.58000', 'fat': '7.28250', 'fiber': '3.24000', 'energy': '208.82700', 'image': '7950d4ad-23eb-4eed-8029-6cab1d29467f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель мини, зелень, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15129, 'combo': False, 'product': {'id': 549, 'name': 'Картофель бэби запеченный 150 гр.', 'price': 79, 'carbohydrate': '32.96700', 'fat': '7.51950', 'fiber': '3.33450', 'energy': '212.88450', 'image': '6aab731e-091e-410d-97a7-9fc4aac4892f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель мини, масло подсолнечное, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15130, 'combo': False, 'product': {'id': 550, 'name': 'Картофель бэби отварной с зеленью 150 гр.', 'price': 79, 'carbohydrate': '29.16564', 'fat': '7.24679', 'fiber': '2.97100', 'energy': '193.76770', 'image': '26388e84-ef95-4742-8ef7-689bec76e4ea.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель мини, масло подсолнечное, соль, перец черный молотый, зелень.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15131, 'combo': False, 'product': {'id': 543, 'name': 'Зеленая гречка с кабачками 150 гр.', 'price': 89, 'carbohydrate': '34.18650', 'fat': '1.56000', 'fiber': '6.82650', 'energy': '178.09200', 'image': 'bae66754-9341-456e-a1cb-d8771329496b.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': ''}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15132, 'combo': False, 'product': {'id': 544, 'name': 'Кабачки на гриле 150 гр.', 'price': 139, 'carbohydrate': '9.84450', 'fat': '0.44850', 'fiber': '1.15650', 'energy': '48.04050', 'image': 'd845dcf7-6b31-47b1-bc9e-bf65003ff711.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: кабачок/цукини, масло подсолнечное, перец черный молотый, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15133, 'combo': False, 'product': {'id': 547, 'name': 'Капуста тушеная с грибами 200 гр.', 'price': 139, 'carbohydrate': '16.35958', 'fat': '14.62295', 'fiber': '3.41380', 'energy': '210.70011', 'image': 'e21c61bd-6076-4919-a945-a489a8dfdc60.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Капуста б/к, морковь,лук репчатый,томатная паста, масло раст.,соль,сахар, перец черный молотый, грибы шампиньоны.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15134, 'combo': False, 'product': {'id': 551, 'name': 'Картофель бэби с грибами 150 гр.', 'price': 79, 'carbohydrate': '29.50935', 'fat': '2.41287', 'fiber': '3.64256', 'energy': '154.32948', 'image': '0eba297e-680e-40e0-a60c-65f0fe92f4fa.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель мини, масло подсолнечное, соль, перец черный молотый, грибы шампиньоны.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15135, 'combo': False, 'product': {'id': 552, 'name': 'Картофель бэби с карри 150 гр.', 'price': 79, 'carbohydrate': '32.58000', 'fat': '2.60250', 'fiber': '3.24000', 'energy': '166.69800', 'image': 'c5818e65-2e43-4cc7-961c-f881c3cd9664.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель мини, масло подсолнечное, соль, перец черный молотый, карри.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15136, 'combo': False, 'product': {'id': 554, 'name': 'Картофель бэби с розмарином 150 гр.', 'price': 79, 'carbohydrate': '32.78700', 'fat': '2.64300', 'fiber': '3.27000', 'energy': '168.01500', 'image': '71465333-2fe9-47f6-97c9-53f035459757.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: картофель мини, масло подсолнечное, соль, перец черный молотый, розмарин.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15137, 'combo': False, 'product': {'id': 555, 'name': 'Картофель жареный 150 гр.', 'price': 89, 'carbohydrate': '33.67950', 'fat': '2.47800', 'fiber': '4.05750', 'energy': '173.25450', 'image': 'd6134279-329f-411b-a7ae-aba1899625b0.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, масло подсолнечное, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15138, 'combo': False, 'product': {'id': 553, 'name': 'Картофель бэби с паприкой 150 гр.', 'price': 79, 'carbohydrate': '32.96250', 'fat': '2.62500', 'fiber': '3.33900', 'energy': '168.83250', 'image': 'f50daab0-a320-4fdf-a575-6235a76a0f60.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель мини, масло подсолнечное, соль, перец черный молотый, паприка.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15139, 'combo': False, 'product': {'id': 561, 'name': 'Картофель запеченный с розмарином 150 гр.', 'price': 89, 'carbohydrate': '27.15000', 'fat': '0.60000', 'fiber': '3.00000', 'energy': '126.00000', 'image': '5d8f4cfe-5a03-471b-b1ca-13d781f7bc79.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель , розмарин , лук репчатый, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15140, 'combo': False, 'product': {'id': 562, 'name': 'Картофель запеченный с травами 150 гр.', 'price': 89, 'carbohydrate': '27.15000', 'fat': '0.60000', 'fiber': '3.00000', 'energy': '126.00000', 'image': '6257e830-e117-4f26-a171-4a4e276e0304.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Картофель,масло раст.,базилик,соль,перец'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15141, 'combo': False, 'product': {'id': 563, 'name': 'Картофель запеченный с шампиньонами 150 гр.', 'price': 89, 'carbohydrate': '26.30250', 'fat': '2.27700', 'fiber': '3.35250', 'energy': '139.11150', 'image': 'fd84c114-e74b-4434-bd98-4160bfd3c8b7.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, грибы шампиньоны , лук репчатый , соль, перец черный молотый, масло подсолнечное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15142, 'combo': False, 'product': {'id': 564, 'name': 'Картофель отварной с зеленью 150 гр.', 'price': 79, 'carbohydrate': '27.36000', 'fat': '7.21800', 'fiber': '2.79150', 'energy': '185.56950', 'image': '80ec915e-2e96-4a6d-ae3c-ae3738a21c67.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: картфель, масло подсолнечное, зелень. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15143, 'combo': False, 'product': {'id': 565, 'name': 'Картофель по-деревенски 150 гр.', 'price': 99, 'carbohydrate': '27.15000', 'fat': '0.60000', 'fiber': '3.00000', 'energy': '126.00000', 'image': '80b0f7bb-9299-4179-997b-6bfd7b1e715e.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: картофель, паприка, соль, перец черный молотый.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15144, 'combo': False, 'product': {'id': 566, 'name': 'Кукуруза с соусом чили 150 гр.', 'price': 119, 'carbohydrate': '28.95000', 'fat': '8.31750', 'fiber': '4.86000', 'energy': '210.10200', 'image': 'b4156f43-da24-48b1-a152-d23193c872df.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: кукуруза , масло подсолнечное, перец черный молотый, соль, перец чили сладкий.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15145, 'combo': False, 'product': {'id': 570, 'name': 'Кускус с овощами 150 гр.', 'price': 109, 'carbohydrate': '29.96100', 'fat': '1.85550', 'fiber': '4.70250', 'energy': '155.34750', 'image': '1028e22d-63cc-45be-8175-ad2b55277909.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: Кус-кус отварной, кабачки , морковь,перец болг., масло раст.,соль'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15146, 'combo': False, 'product': {'id': 572, 'name': 'Овощи на пару 150 гр.', 'price': 149, 'carbohydrate': '4.87950', 'fat': '4.79400', 'fiber': '11.87700', 'energy': '110.17050', 'image': '752c8103-d03c-4075-9df4-b48759a61497.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав:Говяжья вырезка, грибы белые, лук ,карри, соль, перец черный молотый, капуста цветная, кольраби, фасоль стручковая,морковь, перец болгарский, масло оливковое.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15147, 'combo': False, 'product': {'id': 578, 'name': 'Пенне с сыром 150 гр.', 'price': 79, 'carbohydrate': '47.34750', 'fat': '8.00850', 'fiber': '9.06150', 'energy': '297.70800', 'image': 'd675d4dd-3bbc-4662-9457-7300af6e6c2a.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: макароны отварные, сыр " Гауда".'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15148, 'combo': False, 'product': {'id': 1641, 'name': 'Плов с грибами постный 150 гр.', 'price': 89, 'carbohydrate': '26.58000', 'fat': '23.42400', 'fiber': '3.91800', 'energy': '332.80350', 'image': None, 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис, грибы шампиньоны , кинза , кумин, лук репчатый, масло подсолнечное, помидоры, приправа для плова, соль, чеснок.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15149, 'combo': False, 'product': {'id': 584, 'name': 'Рагу из кабачков 150 гр.', 'price': 129, 'carbohydrate': '10.93435', 'fat': '13.73242', 'fiber': '1.53399', 'energy': '173.46666', 'image': '1912d32d-d9af-4c90-8d5a-a24a0302018c.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: кабачки/цукини, зелень, лук репчатый, морковь, помидоры, соль, перец черный молотый, чеснок.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15150, 'combo': False, 'product': {'id': 1887, 'name': 'Рис Басмати с кардомоном 150 гр.', 'price': 119, 'carbohydrate': '51.48150', 'fat': '5.07000', 'fiber': '3.73800', 'energy': '266.50950', 'image': 'cbc507d6-daff-4424-8f17-179db27e261f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: рис Басмати, соль, кардомон.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15151, 'combo': False, 'product': {'id': 1642, 'name': 'Рис с укропом150 гр.', 'price': 69, 'carbohydrate': '47.23619', 'fat': '4.42347', 'fiber': '3.91797', 'energy': '241.06339', 'image': 'fb9a613c-3095-4a6b-a194-5a695b628b90.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Cостав:Рис,шпинат,масло раст.,специи'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15152, 'combo': False, 'product': {'id': 588, 'name': 'Рагу с чечевицей и баклажанами 150 гр.', 'price': 109, 'carbohydrate': '26.82065', 'fat': '1.51525', 'fiber': '9.78315', 'energy': '160.04810', 'image': '9c9e47f1-ce8c-4b6d-b59b-19545e9e1c49.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': ''}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15153, 'combo': False, 'product': {'id': 623, 'name': 'Фасолевый микс с кинзой в томатном соусе 150 гр.', 'price': 109, 'carbohydrate': '24.22650', 'fat': '1.64250', 'fiber': '7.75950', 'energy': '142.72200', 'image': '75bbae21-5a7f-4b6a-a287-1e522cb7b135.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: фасоль, фасоль стручковая, кинза, томатный соус ( лук репчатый, морковь, томатная паста, сельдерей, прованский травы, сахар песок, соль, перец черный молотый).'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15154, 'combo': False, 'product': {'id': 1643, 'name': 'Цветная капуста гриль в панировке 150 гр.', 'price': 119, 'carbohydrate': '22.96500', 'fat': '22.83450', 'fiber': '6.01950', 'energy': '321.45450', 'image': '6b5f63eb-885c-44a9-bab6-45abc58f94df.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: цветная капуста, масло подсолнечное, соль, перец черный молотый, молоко 3,2%, сухари панировочные, яйцо куриное.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15155, 'combo': False, 'product': {'id': 2072, 'name': 'Рис с овощами 150 гр.', 'price': 69, 'carbohydrate': '47.37750', 'fat': '2.40150', 'fiber': '3.55650', 'energy': '225.34500', 'image': '7884c961-f8d6-4740-8019-7662b3353f1f.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: рис отварной, морковь, лук репчатый, кукуруза, горошек зеленый, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15156, 'combo': False, 'product': {'id': 509, 'name': 'Баклажаны на гриле 150 гр.', 'price': 189, 'carbohydrate': '11.63850', 'fat': '0.18000', 'fiber': '2.78100', 'energy': '59.29950', 'image': 'bc7fa4d6-cd91-4cf7-97f1-32f7edf1ba48.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: баклажан, чеснок, соль , перец черный молотый, масло подсолнечное. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15157, 'combo': False, 'product': {'id': 510, 'name': 'Баклажаны печеные с кинзой и чесночным маслом 150 гр.', 'price': 229, 'carbohydrate': '11.67750', 'fat': '0.18750', 'fiber': '2.81850', 'energy': '59.66700', 'image': '638ce80e-c021-4ba6-9b52-fc3f43ceb39f.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: баклажан, кинза, чесночное масло, кинза, перец черный молотый, соль. '}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15158, 'combo': False, 'product': {'id': 537, 'name': 'Гречка отварная 150 гр.', 'price': 59, 'carbohydrate': '32.29200', 'fat': '7.49550', 'fiber': '5.89650', 'energy': '220.21050', 'image': '19a518cc-60c1-4b1c-8160-23d48dbd1070.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: гречневая крупа, масло растительное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15159, 'combo': False, 'product': {'id': 540, 'name': 'Гречка с луком 150 гр.', 'price': 69, 'carbohydrate': '44.59500', 'fat': '7.51950', 'fiber': '7.70550', 'energy': '276.87150', 'image': 'af0aac1d-dfd1-45da-a92a-dc141d1e8c65.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: грибы шампиньоны, гречка, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15160, 'combo': False, 'product': {'id': 559, 'name': 'Картофель запеченный с опятами 150 гр.', 'price': 99, 'carbohydrate': '24.80100', 'fat': '2.38500', 'fiber': '3.23400', 'energy': '133.60650', 'image': 'ff6326aa-574a-4460-a5cf-36d4bc0ddc24.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: картофель , грибы опята, лук репчатый, масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15161, 'combo': False, 'product': {'id': 560, 'name': 'Картофель запеченный с паприкой 150 гр.', 'price': 89, 'carbohydrate': '27.15000', 'fat': '0.60000', 'fiber': '3.00000', 'energy': '126.00000', 'image': 'ed4520ef-d273-4ad7-9a95-dc9673bfb356.jpg', 'vegan': 1, 'allergens': None, 'lactose_free': None, 'sugarless': None, 'gluten_free': None, 'description': 'Состав: картофель , паприка , масло подсолнечное, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15162, 'combo': False, 'product': {'id': 585, 'name': 'Рагу из кабачков с грибами 150 гр.', 'price': 119, 'carbohydrate': '8.18127', 'fat': '13.96184', 'fiber': '2.48467', 'energy': '168.32337', 'image': '5acee879-d402-47d3-a4bd-20d90a7ffa75.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: кабачки/цукини, зелень, лук репчатый, морковь, помидоры, соль, перец черный молотый, чеснок, грибы шампиньоны.'}, 'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 15163, 'combo': False, 'product': {'id': 586, 'name': 'Рагу овощное 150 гр.', 'price': 119, 'carbohydrate': '13.58457', 'fat': '10.39439', 'fiber': '2.85192', 'energy': '159.29250', 'image': 'a5c5540d-8a64-4138-96c5-9b610747e7ba.jpg', 'vegan': 0, 'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0, 'description': 'Состав: капуста б/к, капуста брокколи, картофель, лук репчатый, масло подсолнечное, морковь, перец болгарский, помидоры, чеснок, зелень, соль.'}, 'category': {'id': 9, 'name': 'Гарниры'}}]}}


        js = open("cooking_method.json").read()
        dict_tk = json.loads(js)
        if data_dict['menu']['location']['name'] == 'hadassah':
            load_menu(data_dict, dict_tk)
            load_timetable(data_dict)
            Base.objects.create(base=data_str)
        return Response(data)


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
