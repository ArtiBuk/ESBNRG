from django.contrib import admin

from restaurant.models import Restaurant, RestaurantCategory, Report

admin.site.register(Restaurant)
admin.site.register(RestaurantCategory)
admin.site.register(Report)


