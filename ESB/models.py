# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UserUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RestaurantReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.DateField()
    number_week = models.IntegerField()
    weekdays = models.CharField(max_length=10)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    number_of_checks = models.IntegerField()
    department = models.ForeignKey('RestaurantRestaurant', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'restaurant_report'
        unique_together = (('department', 'data'),)


class RestaurantReporttype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_report = models.CharField(max_length=20)
    short_description = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'restaurant_reporttype'


class RestaurantRestaurant(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=254)
    image = models.CharField(max_length=100)
    short_description = models.CharField(max_length=64)
    city = models.CharField(max_length=10)
    adress = models.CharField(max_length=128)
    category = models.ForeignKey('RestaurantRestaurantcategory', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'restaurant_restaurant'
        unique_together = (('name', 'adress'),)


class RestaurantRestaurantPermGrupFo(models.Model):
    id = models.BigAutoField(primary_key=True)
    restaurant = models.ForeignKey(RestaurantRestaurant, models.DO_NOTHING)
    rightuser = models.ForeignKey('UserRightuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'restaurant_restaurant_perm_grup_fo'
        unique_together = (('restaurant', 'rightuser'),)


class RestaurantRestaurantcategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)
    short_description = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'restaurant_restaurantcategory'


class RestaurantRestaurantcategoryPermGrupForCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    restaurantcategory = models.ForeignKey(RestaurantRestaurantcategory, models.DO_NOTHING)
    rightuser = models.ForeignKey('UserRightuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'restaurant_restaurantcategory_perm_grup_for_category'
        unique_together = (('restaurantcategory', 'rightuser'),)


class UserRightuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)
    where_is_access = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'user_rightuser'


class UserUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    image = models.CharField(max_length=100)
    access_rights = models.ForeignKey(UserRightuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_user'


class UserUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_user_groups'
        unique_together = (('user', 'group'),)


class UserUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_user_user_permissions'
        unique_together = (('user', 'permission'),)
