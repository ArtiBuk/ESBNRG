from django.urls import path

from restaurant.views import restaurant,report

app_name = 'restaurant'

urlpatterns = [
   path('',restaurant,name='index'),
   path('<int:category_id>',restaurant,name='category'),
   path('report/<int:restaurant_id>', report, name='report'),
]