from django.contrib import admin

from restaurant.models import Restaurant, RestaurantCategory, Report, ReportType


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_filter = ('category', 'perm_grup_fo')


admin.site.register(RestaurantCategory)
admin.site.register(ReportType)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_filter = ('department', 'data')
