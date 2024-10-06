from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from content.models import Booking, Room

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
    rooms = Room.objects.all()
    return render(request, "dashboard/room.html", {'rooms': rooms})

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def booking_view(request):
    bookings = Booking.objects.all().order_by('-check_in')
    return render(request, "dashboard/booking.html", {'booking': bookings})


@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def book_form_view(request):
    return render(request, "dashboard/booking-form.html")

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def room_type_view(request):
    return render(request, "dashboard/room-type.html")

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def add_room_view(request):
    return render(request, "dashboard/add-room.html")

