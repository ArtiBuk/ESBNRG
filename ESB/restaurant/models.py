from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import RightUser


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            verbose_name='Название категории')
    short_description = models.CharField(
        max_length=64, blank=True, verbose_name='Краткое описание')
    perm_grup_for_category = models.ManyToManyField(
        RightUser, verbose_name='Группы прав')

    class Meta:
        verbose_name_plural = 'Категории ресторанов'

    def __str__(self):
        return self.name


class CityChoise(models.TextChoices):
    NORILSK = 'Норильск', _('Норильск')
    TALNAH = 'Талнах', _('Талнах')
    KAIR = 'Каейркан', _('Каейркан')
    DUDINKA = 'Дудинка', _('Дудинка')


class Restaurant(models.Model):
    name = models.CharField(max_length=254, verbose_name='Название ресторана')
    image = models.ImageField(
        upload_to='restaurant_images', blank=True, verbose_name='Логотип')
    short_description = models.CharField(
        max_length=64, blank=True, verbose_name='Короткое описание')
    category = models.ForeignKey(
        RestaurantCategory, on_delete=models.PROTECT, verbose_name='Категория ресторана')
    city = models.CharField(max_length=10, blank=False,
                            choices=CityChoise.choices, verbose_name='Город')
    adress = models.CharField(max_length=128, verbose_name='Адресc')
    perm_grup_fo = models.ManyToManyField(
        RightUser, verbose_name='Группы прав')

    class Meta:
        verbose_name_plural = 'Заведения'
        unique_together = ('name', 'adress')

    def __str__(self):
        return f'{self.name} | {self.city} | {self.category.name}'


class WeekDayChoise(models.TextChoices):
    Monday = 'Пн', _('Пн')
    Tuesday = 'Вт', _('Вт')
    Wednesday = 'Ср', _('Ср')
    Thursday = 'Чт', _('Чт')
    Friday = 'Пт', _('Пт')
    Saturday = 'Сб', _('Сб')
    Sunday = 'Вс', _('Вс')


class ReportType(models.Model):
    name_report = models.CharField(max_length=20, verbose_name='Вид отчета')
    short_description = models.CharField(
        max_length=64, blank=True, verbose_name='Краткое описание отчета')

    class Meta:
        verbose_name_plural = 'Виды отчета'

    def __str__(self):
        return f'{self.name_report} | {self.short_description} '


class Report(models.Model):
    department = models.ForeignKey(
        Restaurant, on_delete=models.PROTECT, verbose_name='Наименование ресторана')
    data = models.DateField(verbose_name='Дата')
    number_week = models.IntegerField(verbose_name='№ недели')
    weekdays = models.CharField(max_length=10,
                                choices=WeekDayChoise.choices, verbose_name='День недели')
    revenue = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Выручка')
    cost_price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Себестоимость')
    number_of_checks = models.IntegerField(verbose_name='Количество чеков')

    class Meta:
        verbose_name_plural = 'Данные для отчетов'
        unique_together = ('department', 'data')

    def __str__(self):
        return f'{self.department} | {self.data}'
