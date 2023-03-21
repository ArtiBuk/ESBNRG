from django.db import models
from django.utils.translation import gettext_lazy as _

class RestaurantCategory(models.Model):
    name = models.CharField(max_length=64,unique=True,verbose_name='Название категории')
    short_description = models.CharField(max_length=64,blank=True,verbose_name='Краткое описание')
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
    name = models.CharField(max_length=254,verbose_name='Название ресторана')
    image = models.ImageField(upload_to='restaurant_images', blank=True, verbose_name='Логотип')
    short_description = models.CharField(max_length=64, blank=True, verbose_name='Короткое описание')
    category = models.ForeignKey(RestaurantCategory, on_delete=models.PROTECT, verbose_name='Категория ресторана')
    city = models.CharField(max_length=10, blank=False,choices=CityChoise.choices, verbose_name='Город')
    adress = models.CharField(max_length=128, verbose_name='Адрес') 
    class Meta:
        verbose_name_plural = 'Заведения'
    
    def __str__(self):
        return f'{self.name} | {self.category.name}'
