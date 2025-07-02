from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import User

def login_view(request):
    if request.method == 'POST':
        u = request.POST['username']; p = request.POST['password']
        if not u or not p:
            messages.error(request,'Fill all fields')
            return redirect('login')
        user = authenticate(request, username=u, password=p)
        if not user:
            messages.error(request,'Invalid credentials')
            return redirect('login')
        django_login(request,user)
        return redirect('home')
    return render(request,'registration/login.html')

def signup_view(request):
    if request.method=='POST':
        u=request.POST['username']; p=request.POST['password']
        if not u or not p:
            messages.error(request,'Fill all fields')
            return redirect('signup')
        if User.objects.filter(username=u).exists():
            messages.error(request,'User exists')
            return redirect('signup')
        User.objects.create_user(username=u,password=p)
        messages.success(request,'Signed up')
        return redirect('login')
    return render(request,'registration/signup.html')

@login_required
def logout_view(request):
    django_logout(request)
    return redirect('home')