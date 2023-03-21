from django.shortcuts import render

from restaurant.models import Restaurant,RestaurantCategory

def index(request):
    context = {
        'title': 'NRG'
    }
    return render(request, 'restaurant/index.html',context)

def restaurant(request):
    context = {
        'title': 'restaurant',
        'categories': RestaurantCategory.objects.all(),
        'restaurant': Restaurant.objects.all(),
    }
    return render(request, 'restaurant/restaurant.html',context)

