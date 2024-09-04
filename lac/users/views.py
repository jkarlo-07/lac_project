from django.core.mail import BadHeaderError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import CustomUser
from lac.utils.email_utils import send_email_contact
import random

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                
                if user.is_staff:
                    return redirect("dashboard:dashboard")
                else:
                    return redirect('content:book_1')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)  
            return redirect('users:signupsuc') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, "users/signup.html", {"form": form})

def signupsuc_view(request):
    return render(request, "users/sign-up-successful.html")

def forgot_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                username = user.username
                random_code = random.randint(1000, 9999)
                user.email_confirm_code = random_code
                user.save()
                try:
                    result = send_email_contact(username, email, "Password Account Recovery", random_code, email, 'users/user_forgot_email.html')
                    
                    if result['success']:
                        return redirect("users:login")
                    else:
                        return JsonResponse({'error': result['error']}, status=500)             
                except BadHeaderError:
                    return JsonResponse({'error': 'Invalid header found.'}, status=400)
                
                except Exception as e:
                    return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
            except CustomUser.DoesNotExist:
                messages.error(request, "No user found within this email")
    return render(request, "users/forgot-password.html")

def pin_view(request):
    return render(request, "users/pin-forgot.html")

def newpass_view(request):
    return render(request, "users/newpass.html")

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")
    
