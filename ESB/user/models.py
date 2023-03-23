from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='user_images', blank=True, verbose_name='Аватарка')
    class Meta:
        verbose_name_plural = 'Пользователи'
