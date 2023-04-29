from django.urls import path
from restaurant.views import restaurant, report, search_restaurant

app_name = 'restaurant'

urlpatterns = [
   path('', restaurant, name='index'),
   path('<int:category_id>', restaurant, name='category'),
   path('<int:access_id>', restaurant, name='perm'),
   path('report/<int:restaurant_id>', report, name='report'),
   path('page/<int:page>', restaurant, name='restaurant_pagination'),
   path('search/', search_restaurant, name='search_restaurant'),
   path('report/<int:restaurant_id>/<int:report_type_id>/', report, name='report_type')
]