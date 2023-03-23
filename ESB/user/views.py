from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from user.forms import UserLoginForm,UserRegistrationForm,UserProfileForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request,'user/login.html',context)

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'user/register.html',context)

def profile(request):
    if request.method == "POST":
        form = UserProfileForm(data = request.POST,files = request.FILES ,instance = request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form':form}
    return render(request,'user/profile.html',context)