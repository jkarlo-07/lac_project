from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_staff(user):
    return user.is_staff

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def guest_view(request):
    return render(request, "dashboard/guest.html")

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def room_view(request):
    return render(request, "dashboard/room.html")

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def booking_view(request):
    return render(request, "dashboard/booking.html")
