from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class RightUser(models.Model):
    name = models.CharField(max_length=64,unique=True,verbose_name='Название права доступа')
    where_is_access = models.CharField(max_length=64,blank=True,verbose_name='Куда имеется доступ')
    class Meta:
        verbose_name_plural = 'Права доступа'
    
    def __str__(self):
        return f'{self.name}'
  
class User(AbstractUser):
    image = models.ImageField(upload_to='user_images', blank=True, verbose_name='Аватарка')
    access_rights = models.ForeignKey(RightUser, on_delete=models.PROTECT, verbose_name='Права доступа пользователя',blank=True,default=25)
    class Meta:
        verbose_name_plural = 'Пользователи'
    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.access_rights}'