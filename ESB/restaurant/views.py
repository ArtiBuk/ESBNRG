from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant,RestaurantCategory


def index(request):
    context = {
        'title': 'NRG'
    }
    return render(request, 'restaurant/index.html',context)

@login_required
def restaurant(request,category_id=None):
    context = {
        'title': 'restaurant',
        'categories': RestaurantCategory.objects.all()
    }
    if category_id:
        context.update({
           'restaurant': Restaurant.objects.filter(category_id=category_id) 
        })
    else:
        context.update({
            'restaurant': Restaurant.objects.all()
        })
    return render(request, 'restaurant/restaurant.html',context)

def report(request,restaurant_id):
    context = {
        'title' : Restaurant.objects.get(id = restaurant_id).name,
        'category': Restaurant.objects.get(id = restaurant_id).category,
        'city' : Restaurant.objects.get(id = restaurant_id).city,
        'address' : Restaurant.objects.get(id = restaurant_id).adress
    }
    return render(request, 'restaurant/report.html',context)

