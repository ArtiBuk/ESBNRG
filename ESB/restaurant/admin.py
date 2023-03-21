from django.contrib import admin

from restaurant.models import Restaurant, RestaurantCategory

admin.site.register(Restaurant)
admin.site.register(RestaurantCategory)
