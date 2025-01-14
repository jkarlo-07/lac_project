from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout, update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import BadHeaderError
from django.http import JsonResponse
from django.shortcuts import render, redirect

import random

from .forms import CustomUserCreationForm, NewPasswordForm
from .models import CustomUser
from lac.utils.email_utils import send_email_contact


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Get the 'next' parameter from the query string or from the POST request
                next_url = request.session.get('next_url', '/')
                print('hey', next_url)
                if next_url:
                    # Redirect to the captured 'next' URL (if available), otherwise redirect to home
                    return redirect(next_url)
                
                # If no 'next' URL, redirect based on user type
                if user.is_staff:
                    return redirect("dashboard:dashboard")
                else:
                    return redirect('content:calendar')
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
                        request.session['reset_user_id'] = user.id
                        return redirect("users:pin")
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
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect("users:forgot")
    
    user = CustomUser.objects.get(id=user_id)
    user_code = str(user.email_confirm_code) 
    if request.method == "POST":
        input_code = request.POST.get("code")   
        if input_code:
            if input_code == user_code:
                return redirect("users:newpass")
            else:
                messages.error(request, "The code you entered is incorrect.")
        else:
            messages.error(request, "Please enter a valid code.")
        return redirect("users:pin") 
    
    return render(request, "users/pin-forgot.html")

def newpass_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect("users:forgot")

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.email_confirm_code = None
            user.save()
            update_session_auth_hash(request, user)
            request.session.flush()
            return redirect("users:login")
    else:
        form = NewPasswordForm()

    return render(request, "users/newpass.html", {'form': form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")
    
def resend_pin_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect("users:forgot")
    user = CustomUser.objects.get(id=user_id)
    email = user.email
    username = user.username
    random_code = random.randint(1000, 9999)
    user.email_confirm_code = random_code
    user.save()
    try:
        result = send_email_contact(username, email, "Password Account Recovery", random_code, email, 'users/user_forgot_email.html')
                    
        if result['success']:
            request.session['reset_user_id'] = user.id
            return redirect("users:pin")
        else:
            return JsonResponse({'error': result['error']}, status=500)             
    except BadHeaderError:
        return JsonResponse({'error': 'Invalid header found.'}, status=400)
                
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    except CustomUser.DoesNotExist:
        messages.error(request, "No user found within this email")
    
    