from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant,RestaurantCategory
from user.models import User,RightUser
from django.db.models import Q


def index(request):
    context = {
        'title': 'NRG'
    }
    return render(request, 'restaurant/index.html',context)

@login_required
def restaurant(request, category_id=None):
    user = request.user
    # Получаем доступные для пользователя категории ресторанов
    categories = RestaurantCategory.objects.filter(perm_grup_for_category=user.access_rights)
    context = {
        'title': 'restaurant',
        'categories': categories,
    }
    # Фильтруем рестораны, принадлежащие выбранной категории и доступные для пользователя
    if category_id:
        restaurants = Restaurant.objects.filter(category_id=category_id, perm_grup_fo=user.access_rights)
    # Если категория не выбрана, выводим все доступные рестораны для пользователя
    else:
        restaurants = Restaurant.objects.filter(perm_grup_fo=user.access_rights)
    context.update({
        'restaurant': restaurants,
    })
    return render(request, 'restaurant/restaurant.html', context)

def report(request,restaurant_id):
    context = {
        'title' : Restaurant.objects.get(id = restaurant_id).name,
        'category': Restaurant.objects.get(id = restaurant_id).category,
        'city' : Restaurant.objects.get(id = restaurant_id).city,
        'address' : Restaurant.objects.get(id = restaurant_id).adress
    }
    return render(request, 'restaurant/report.html',context)

