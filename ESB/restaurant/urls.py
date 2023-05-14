from django.urls import path
from restaurant.views import restaurant, consolidated_report, search_restaurant, week_report, mounth_report

app_name = 'restaurant'

urlpatterns = [
     path('', restaurant, name='index'),
     path('<int:category_id>', restaurant, name='category'),
     path('<int:access_id>', restaurant, name='perm'),
     path('page/<int:page>', restaurant, name='restaurant_pagination'),
     path('search/', search_restaurant, name='search_restaurant'),
     path('consolidated_report/<int:report_type_id>/',
          consolidated_report, name='report_type'),
     path('week_results/<int:report_type_id>/',
          week_report, name='week_results'),
     path('mounth_results/<int:report_type_id>/',
          mounth_report, name='mounth_results'),
]
