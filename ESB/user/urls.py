from django.urls import path

from user.views import login, register,profile

app_name = 'user'

urlpatterns = [
   path('login/',login,name='login'),
   path('register/',register,name='register'),
   path('profile/',profile,name='profile')
]