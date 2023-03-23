from django.urls import path

from user.views import login, register

app_name = 'user'

urlpatterns = [
   path('login/',login,name='login'),
   path('register/',register,name='register')
]