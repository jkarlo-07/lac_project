from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def login_view(request):
    return render(request, "users/login.html")

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('users:login') 
    else:
        form = UserCreationForm()
    
    return render(request, "users/signup.html", {"form": form})

def signupsuc_view(request):
    return render(request, "users/sign-up-successful.html")