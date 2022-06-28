from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Base, Product, Timetable
from .forms import UserRegistrationForm, UserloginForm, TimetableForm
from django.forms import modelformset_factory

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


def index(request):
    error = ''
    ProductFormSet = modelformset_factory(Product,
                                          fields=(
                                              'iditem', 'name', 'description', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd',
                                              'vkd', 'carbohydrate', 'fat', 'fiber', 'energy', 'category'),
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
            queryset_main_dishes = Product.objects.filter(timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(
                category='Вторые блюда')
            queryset_side_dishes = Product.objects.filter(timetable__datetime=str(form_date.cleaned_data["datetime"])).filter(category='Гарниры')

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
        formset_main_dishes = ProductFormSet(queryset=queryset_salad, prefix='main_dishes')
        formset_side_dishes = ProductFormSet(queryset=queryset_soup, prefix='side_dishes')

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
        # data_dict = {
        #     'menu': {'id': 682, 'date': '27.06.2022', 'status': 'completed', 'completed_at': '22.06.2022 17:52:31',
        #              'created_at': '17.06.2022 10:26:17', 'combo_price': 350,
        #              'location': {'id': 4, 'name': 'hadassah', 'subdomain': 'hadassah'}, 'items': [
        #             {'id': 13276, 'combo': False,
        #              'product': {'id': 251, 'name': 'Говядина по-азиатски 75/75 гр.', 'price': 239,
        #                          'carbohydrate': '0.57539', 'fat': '11.42332', 'fiber': '21.60205',
        #                          'energy': '191.51808', 'image': 'a8faed5c-fd3e-40cf-bb93-6d86240a268e.jpg', 'vegan': 0,
        #                          'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0,
        #                          'description': 'Состав: говядина, масло подсолнечное, соус соевый, крахмал, соус терияки, перец чили, масло кунжутное, кунжут, корень имбиря, перец болгарский, лук репчатый.'},
        #              'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13277, 'combo': False,
        #                                                               'product': {'id': 337,
        #                                                                           'name': 'Куриная ватрушка с грибным жульеном 120 гр.',
        #                                                                           'price': 159,
        #                                                                           'carbohydrate': '23.04720',
        #                                                                           'fat': '17.42760',
        #                                                                           'fiber': '20.17560',
        #                                                                           'energy': '329.73120',
        #                                                                           'image': '66366171-300e-469f-8692-de7da76785f4.jpg',
        #                                                                           'vegan': 0, 'allergens': 0,
        #                                                                           'lactose_free': 0, 'sugarless': 0,
        #                                                                           'gluten_free': 0,
        #                                                                           'description': 'Состав : Состав : фарш из курицы ( филе курицы, хлеб, соль, перекц , лук репчатый), масло подсолнечное, сыр Гауда, жульен грибной ( грибы шампиньоны, лук репчатый, масло подсолнечное, молоко 3,2%, сливки 33%, перец черный молотый, соль).'},
        #                                                               'category': {'id': 6, 'name': 'Вторые блюда'}},
        #             {'id': 13278, 'combo': False,
        #              'product': {'id': 396, 'name': 'Перец фаршированный овощами, грибами и кус-кусом 200/50',
        #                          'price': 239, 'carbohydrate': '25.70250', 'fat': '8.97750', 'fiber': '4.95250',
        #                          'energy': '203.40750', 'image': '7bba3000-acb3-4b5d-aecd-aa0b7be477e5.jpg', 'vegan': 0,
        #                          'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0,
        #                          'description': 'Состав: перец болгарский, грибы шампиньоны, кускус, морковь, перец болгарский, томатный соус ( томатная паста, лук репчатый, морковь, перец черный молотый, соль, прованские травы),'},
        #              'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13279, 'combo': True,
        #                                                               'product': {'id': 1817,
        #                                                                           'name': 'Суп-крем овощной 250 гр.',
        #                                                                           'price': 99,
        #                                                                           'carbohydrate': '21.50694',
        #                                                                           'fat': '5.40708', 'fiber': '2.86319',
        #                                                                           'energy': '146.14958',
        #                                                                           'image': 'fb998852-3579-4a9a-bba7-abe5cccb8f32.jpg',
        #                                                                           'vegan': 0, 'allergens': 0,
        #                                                                           'lactose_free': 0, 'sugarless': 0,
        #                                                                           'gluten_free': 0,
        #                                                                           'description': 'Состав: капуста брокколи, капуста цветная , лук репчатый, картофель, морковь, зхелень, сельдерей, перец, соль, масло оливковое, сливки 33 % .'},
        #                                                               'category': {'id': 17, 'name': 'Первые блюда'}},
        #             {'id': 13280, 'combo': False,
        #              'product': {'id': 1255, 'name': 'Тайский суп с лапшой и говядиной 250 гр.', 'price': 169,
        #                          'carbohydrate': '17.91500', 'fat': '14.48250', 'fiber': '15.07500',
        #                          'energy': '262.29000', 'image': '76113578-d361-41f9-9bad-31a37e26c856.jpg', 'vegan': 0,
        #                          'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0,
        #                          'description': 'Состав: шпинат, говядина, чеснок, имбирь, лук репчатый, морковь, масло подсолнечное, грибы шампиньоны, лапша гречневая, соевый соус, соль, перец.'},
        #              'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13281, 'combo': False,
        #                                                                'product': {'id': 434,
        #                                                                            'name': 'Стейк из бедра индейки с томатной сальсой 100/50 гр.',
        #                                                                            'price': 239,
        #                                                                            'carbohydrate': '3.64950',
        #                                                                            'fat': '16.14150',
        #                                                                            'fiber': '21.92400',
        #                                                                            'energy': '247.57050',
        #                                                                            'image': 'df5fb311-1b7f-4373-bc4d-2ca869c8b3e7.jpg',
        #                                                                            'vegan': 0, 'allergens': 0,
        #                                                                            'lactose_free': 0, 'sugarless': 0,
        #                                                                            'gluten_free': 0,
        #                                                                            'description': 'Состав : филе индейки, соевый соус, тимьян, мед, масло подсолнечное, томатная сальса( помидор, лук репчатый, чеснок, кинза, соль, перец, масло оливковое).'},
        #                                                                'category': {'id': 6, 'name': 'Вторые блюда'}},
        #             {'id': 13282, 'combo': True,
        #              'product': {'id': 446, 'name': 'Тефтели куриные с зеленым горошком в сметанном соусе 100/50гр.',
        #                          'price': 139, 'carbohydrate': '16.39800', 'fat': '12.20250', 'fiber': '14.38200',
        #                          'energy': '232.92450', 'image': '1b066181-48e5-4739-b847-6819afa21f54.jpg', 'vegan': 0,
        #                          'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0,
        #                          'description': 'Состав: фарш куриный (курица, соль, перец, лук, хлеб),горек зеленый, сметана, мука пшеничная, соль,перец черный молотый.'},
        #              'category': {'id': 6, 'name': 'Вторые блюда'}}, {'id': 13283, 'combo': False,
        #                                                               'product': {'id': 514,
        #                                                                           'name': 'Брокколи на пару с болгарским перцем 150 гр.',
        #                                                                           'price': 119,
        #                                                                           'carbohydrate': '7.41150',
        #                                                                           'fat': '5.26650', 'fiber': '3.73650',
        #                                                                           'energy': '91.98150',
        #                                                                           'image': '0f3a5af0-8454-4441-a5f6-c53655b1b2b3.jpg',
        #                                                                           'vegan': 1, 'allergens': 0,
        #                                                                           'lactose_free': None,
        #                                                                           'sugarless': None,
        #                                                                           'gluten_free': None,
        #                                                                           'description': 'Состав:Капуста брокколи с/м, перец болгарский, масло подсолнечное'},
        #                                                               'category': {'id': 9, 'name': 'Гарниры'}},
        #             {'id': 13284, 'combo': True,
        #              'product': {'id': 617, 'name': 'Спагетти отварные 150 гр.', 'price': 69,
        #                          'carbohydrate': '35.74950', 'fat': '7.15650', 'fiber': '4.68000',
        #                          'energy': '226.12350', 'image': '66149542-2a5f-426e-9e58-bf327a581b76.jpg', 'vegan': 1,
        #                          'allergens': 0, 'lactose_free': None, 'sugarless': None, 'gluten_free': None,
        #                          'description': 'Состав Спагетти, масло подс.,соль.'},
        #              'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13285, 'combo': False, 'product': {'id': 359,
        #                                                                                                   'name': 'Лазанья грибная 200 гр.',
        #                                                                                                   'price': 199,
        #                                                                                                   'carbohydrate': '56.29400',
        #                                                                                                   'fat': '14.49800',
        #                                                                                                   'fiber': '19.03600',
        #                                                                                                   'energy': '431.79400',
        #                                                                                                   'image': 'f82d609c-7824-4492-b297-a0616726f9cb.jpg',
        #                                                                                                   'vegan': 0,
        #                                                                                                   'allergens': 0,
        #                                                                                                   'lactose_free': 0,
        #                                                                                                   'sugarless': 0,
        #                                                                                                   'gluten_free': 0,
        #                                                                                                   'description': 'Состав : грибы шампиньоны, лук репчатый, масло подсолнечное, паста для лазаньи, перец черный молотый, соль, сыр гауда, соус бешамель ( масло сливочное, молоко 3,2%, мускатный орех, мука пшеничная, соль, перец черный молотый.)'},
        #                                                          'category': {'id': 6, 'name': 'Вторые блюда'}},
        #             {'id': 13286, 'combo': False,
        #              'product': {'id': 1218, 'name': 'Суп рисовый с куриными фрикадельками 250 гр.', 'price': 89,
        #                          'carbohydrate': '10.14000', 'fat': '4.60750', 'fiber': '6.47750',
        #                          'energy': '107.94000', 'image': 'dd6bbb7a-d17c-4725-b8b8-2da02e2012db.jpg', 'vegan': 0,
        #                          'allergens': 0, 'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0,
        #                          'description': 'Состав Бульон куриный, фрикадельки из куриного фарша,рис, морковь, лук репчатый,соль , перец'},
        #              'category': {'id': 17, 'name': 'Первые блюда'}}, {'id': 13287, 'combo': False,
        #                                                                'product': {'id': 508,
        #                                                                            'name': ' Картофельное пюре со шпинатом150 гр.',
        #                                                                            'price': 89,
        #                                                                            'carbohydrate': '26.91450',
        #                                                                            'fat': '7.95750', 'fiber': '4.05450',
        #                                                                            'energy': '195.50250',
        #                                                                            'image': 'ee560f38-5b7b-41f8-8275-a4a2b3e7f8b1.jpg',
        #                                                                            'vegan': 0, 'allergens': 0,
        #                                                                            'lactose_free': 0, 'sugarless': 0,
        #                                                                            'gluten_free': 0,
        #                                                                            'description': 'Состав: Картофель,молоко,масло сливочное,шпинат с/м.,соль'},
        #                                                                'category': {'id': 9, 'name': 'Гарниры'}},
        #             {'id': 13288, 'combo': False,
        #              'product': {'id': 1642, 'name': 'Рис с укропом150 гр.', 'price': 69, 'carbohydrate': '47.23619',
        #                          'fat': '4.42347', 'fiber': '3.91797', 'energy': '241.06339',
        #                          'image': 'fb9a613c-3095-4a6b-a194-5a695b628b90.jpg', 'vegan': 0, 'allergens': 0,
        #                          'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0,
        #                          'description': 'Cостав:Рис,шпинат,масло раст.,специи'},
        #              'category': {'id': 9, 'name': 'Гарниры'}}, {'id': 13289, 'combo': False, 'product': {'id': 927,
        #                                                                                                   'name': 'Салат "Столичный" с курицей 100 гр.',
        #                                                                                                   'price': 89,
        #                                                                                                   'carbohydrate': '5.98515',
        #                                                                                                   'fat': '9.44750',
        #                                                                                                   'fiber': '6.03912',
        #                                                                                                   'energy': '133.12458',
        #                                                                                                   'image': '298406ab-7fd7-4b54-8c47-ac94ea3ac828.jpg',
        #                                                                                                   'vegan': 0,
        #                                                                                                   'allergens': 0,
        #                                                                                                   'lactose_free': 0,
        #                                                                                                   'sugarless': 0,
        #                                                                                                   'gluten_free': 0,
        #                                                                                                   'description': 'Состав: картофель, морковь, филе куриное, огурцы маринованные, огурцы свежие, горошек консерв, яйцо куриное отварное, майонез, зелень, соль.'},
        #                                                          'category': {'id': 15, 'name': 'Салаты'}},
        #             {'id': 13290, 'combo': False,
        #              'product': {'id': 947, 'name': 'Салат из крабовых палочек 100 гр.', 'price': 89,
        #                          'carbohydrate': '5.40000', 'fat': '9.16500', 'fiber': '2.91000', 'energy': '115.72500',
        #                          'image': '606430d1-cf3b-4d6d-ac82-050ed6bf6bd0.jpg', 'vegan': 0, 'allergens': 0,
        #                          'lactose_free': 0, 'sugarless': 0, 'gluten_free': 0,
        #                          'description': 'Состав: Огурцы свежие, капуста пекинская, крабовые палочки,масйонез, кукуруза консервированная.'},
        #              'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13291, 'combo': False, 'product': {'id': 992,
        #                                                                                                   'name': 'Салат из томатов с редисом 100 гр.',
        #                                                                                                   'price': 109,
        #                                                                                                   'carbohydrate': '3.58000',
        #                                                                                                   'fat': '5.16000',
        #                                                                                                   'fiber': '0.80500',
        #                                                                                                   'energy': '63.98000',
        #                                                                                                   'image': '1c25edbd-0443-4865-a7e0-ba0c9417e44f.jpg',
        #                                                                                                   'vegan': 0,
        #                                                                                                   'allergens': 0,
        #                                                                                                   'lactose_free': 0,
        #                                                                                                   'sugarless': 0,
        #                                                                                                   'gluten_free': 0,
        #                                                                                                   'description': 'Состав:Помидоры свежие, редис, укроп, масло раст., соль.'},
        #                                                          'category': {'id': 15, 'name': 'Салаты'}},
        #             {'id': 13292, 'combo': True,
        #              'product': {'id': 976, 'name': 'Салат из свежей капусты с зеленым горошком 100 гр.', 'price': 79,
        #                          'carbohydrate': '4.82248', 'fat': '7.27273', 'fiber': '2.26123', 'energy': '93.78938',
        #                          'image': '5f3ea239-a7b2-47e8-9de5-3ca456a6e175.jpg', 'vegan': 1, 'allergens': 0,
        #                          'lactose_free': None, 'sugarless': None, 'gluten_free': None,
        #                          'description': 'Состав:Капуста белокачанная, горошек консерв., зелень, масло раст., соль.'},
        #              'category': {'id': 15, 'name': 'Салаты'}}, {'id': 13293, 'combo': False, 'product': {'id': 958,
        #                                                                                                   'name': 'Салат из огурцов с укропом 100 гр.',
        #                                                                                                   'price': 89,
        #                                                                                                   'carbohydrate': '2.87000',
        #                                                                                                   'fat': '2.12600',
        #                                                                                                   'fiber': '0.86200',
        #                                                                                                   'energy': '34.06200',
        #                                                                                                   'image': 'cc924895-5a6e-49d3-b344-13173340541a.jpg',
        #                                                                                                   'vegan': 1,
        #                                                                                                   'allergens': None,
        #                                                                                                   'lactose_free': None,
        #                                                                                                   'sugarless': None,
        #                                                                                                   'gluten_free': None,
        #                                                                                                   'description': 'Cостав:Огурцы свежие, укроп,масло раст.,соль'},
        #                                                          'category': {'id': 15, 'name': 'Салаты'}}]}}
        load_menu(data_dict)
        load_timetable(data_dict)
        Base.objects.create(base=data_str)
        return Response(data)


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

            if payload['username'] == response.get(
                    'username'):  # если имя пользователя есть в ответе регестрация прошла успешно
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
            return HttpResponseRedirect(reverse('app_name:index'))
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
