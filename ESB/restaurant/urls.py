from django.urls import path

from restaurant.views import restaurant

app_name = 'restaurant'

urlpatterns = [
   path('',restaurant,name='index'),
   path('<int:category_id>',restaurant,name='category'),
]