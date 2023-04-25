from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant, RestaurantCategory, Report
from user.models import User, RightUser
from django.db.models import Q
from django.core.paginator import Paginator
import openpyxl


def index(request):
    context = {
        'title': 'NRG'
    }
    return render(request, 'restaurant/index.html', context)


@login_required
def restaurant(request, category_id=None):
    user = request.user
    # Получаем доступные для пользователя категории ресторанов
    categories = RestaurantCategory.objects.filter(
        perm_grup_for_category=user.access_rights)
    context = {
        'title': 'restaurant',
        'categories': categories,
    }
    # Фильтруем рестораны, принадлежащие выбранной категории и доступные для пользователя
    if category_id:
        restaurants = Restaurant.objects.filter(
            category_id=category_id, perm_grup_fo=user.access_rights)
    # Если категория не выбрана, выводим все доступные рестораны для пользователя
    else:
        restaurants = Restaurant.objects.filter(
            perm_grup_fo=user.access_rights)

    paginator = Paginator(restaurants, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({
        'restaurant': page_obj,
    })
    return render(request, 'restaurant/restaurant.html', context)

# def report(request,restaurant_id):
#     context = {
#         'title' : Restaurant.objects.get(id = restaurant_id).name,
#         'category': Restaurant.objects.get(id = restaurant_id).category,
#         'city' : Restaurant.objects.get(id = restaurant_id).city,
#         'address' : Restaurant.objects.get(id = restaurant_id).adress
#     }
#     return render(request, 'restaurant/report.html',context)


def report(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    workbook = openpyxl.load_workbook(
        '/home/artibuk/Документы/src/ESBNRG/base.xlsx')
    # предположим, что имя листа совпадает с названием ресторана
    worksheet = workbook['РН']

    reports = []  # список для хранения созданных записей в модели Report

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        if all(row):
            data_str = row[5].strftime('%Y-%m-%d')
            number_week = row[3]
            weekdays = row[4]
            revenue = row[6]
            cost_price = row[7]
            number_of_checks = row[8]

            report, created = Report.objects.update_or_create(data=data_str, number_week=number_week, weekdays=weekdays,
                                                              revenue=revenue, cost_price=cost_price, number_of_checks=number_of_checks, defaults={'department': restaurant})
            if not created:
                # Объект уже существовал, ничего не делаем
                continue
            reports.append(report)

    # bulk_create() позволяет создать множество записей в одном запросе
    Report.objects.bulk_create(reports)

    context = {
        'title': restaurant.name,
        'category': restaurant.category,
        'city': restaurant.city,
        'address': restaurant.adress,
    }
    return render(request, 'restaurant/report.html', context)
