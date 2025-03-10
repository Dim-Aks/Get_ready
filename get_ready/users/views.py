from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_user(request):
    if request.method == 'POST':
        username = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html')
    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')

def register(request):
    return render(request, 'users/register.html')

