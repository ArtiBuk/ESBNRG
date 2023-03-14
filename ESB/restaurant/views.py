from django.shortcuts import render

def index(request):
    context = {
        'title': 'NRG'
    }
    return render(request, 'restaurant/index.html',context)

def restaurant(request):
    context = {
        'title': 'restaurant'
    }
    return render(request, 'restaurant/restaurant.html',context)

def test_context(request):
    return render(request, '')
