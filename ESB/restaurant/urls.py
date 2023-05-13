from django.urls import path
from restaurant.views import restaurant, consolidated_report, search_restaurant, report_week_and_mounth

app_name = 'restaurant'

urlpatterns = [
    path('', restaurant, name='index'),
    path('<int:category_id>', restaurant, name='category'),
    path('<int:access_id>', restaurant, name='perm'),
    path('page/<int:page>', restaurant, name='restaurant_pagination'),
    path('search/', search_restaurant, name='search_restaurant'),
    path('consolidated_report/<int:report_type_id>/',
         consolidated_report, name='report_type'),
    path('week_mounth_results/<int:report_type_id>/',
         report_week_and_mounth, name='week_mounth_results'),
]
