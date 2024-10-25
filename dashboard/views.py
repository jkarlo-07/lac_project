from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from content.models import Booking, Room, Guest, RoomType
from django.http import JsonResponse
from django.db.models import Count
from datetime import datetime, timedelta

def is_staff(user):
    return user.is_staff

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def guest_view(request):
    guests = Guest.objects.all()
    return render(request, "dashboard/guest.html", {'guests' : guests})

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

def total_amount_per_month():
    today = datetime.today()

    last_six_months = []
    total_amounts = []

    for i in range(6):
        month_date = today - timedelta(days=30 * i)
        last_six_months.append(month_date.strftime('%B'))  
        total_amounts.append(0)  

    bookings = Booking.objects.filter(check_in__gte=today - timedelta(days=180)) 

    for booking in bookings:
        month = booking.check_in.strftime('%B') 
        if month in last_six_months:
            index = last_six_months.index(month)
            total_amounts[index] += booking.total_amount

    last_six_months.reverse()
    total_amounts.reverse()

    return last_six_months, total_amounts

def sample_sales_data(request):
    room_types_with_bookings = RoomType.objects.annotate(booking_count=Count('room__booking'))

    room_labels = []
    room_bookings = []

    for room_type in room_types_with_bookings:
        room_labels.append(room_type.room_type)
        room_bookings.append(room_type.booking_count)

    sales_months, sales_amounts = total_amount_per_month()

    data = {
        'room_labels': room_labels,      
        'room_bookings': room_bookings, 
        'sales_months': sales_months, 
        'sales_amounts': sales_amounts,    
    }
    
    return JsonResponse(data)