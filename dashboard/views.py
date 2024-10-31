from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from content.models import Booking, Room, Guest, RoomType
from django.http import JsonResponse
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .forms import ExistingRoomForm
from django.contrib import messages


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
    roomtypes = RoomType.objects.all()
    return render(request, "dashboard/room.html", {'rooms': rooms, 'roomtypes': roomtypes, 'show_form': True  })

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
    today = datetime.now()

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

def booking_count_per_month():
    today = datetime.now()

    last_six_months = []
    booking_counts = [0] * 6  

    for i in range(6):
        month_date = today - timedelta(days=30 * i)
        last_six_months.append(month_date.strftime('%B'))

    last_six_months.reverse()
    booking_counts.reverse()

    bookings = Booking.objects.filter(check_in__gte=today - timedelta(days=180))

    for booking in bookings:
        month = booking.check_in.strftime('%B')
        if month in last_six_months:
            index = last_six_months.index(month)
            booking_counts[index] += 1  

    return last_six_months, booking_counts

def booking_count_per_month_past():
    today = datetime.now()

    last_six_months = []
    booking_counts = [0] * 6

    for i in range(5, -1, -1):  
        month_date = today.replace(year=today.year - 1) - relativedelta(months=i)
        last_six_months.append(month_date.strftime('%B %Y'))

    bookings = Booking.objects.filter(
        check_in__year=today.year - 1,
        check_in__month__in=[datetime.strptime(month, '%B %Y').month for month in last_six_months]
    )

    for booking in bookings:
        month_year = booking.check_in.strftime('%B %Y')
        if month_year in last_six_months:
            index = last_six_months.index(month_year)
            booking_counts[index] += 1 

    return booking_counts


from django.db.models import Q
from datetime import datetime, timedelta


def count_available_rooms():
    available_rooms_12h = set()  
    
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    start_hour = current_hour + (1 if current_minute >= 30 else 0)

    end_time = 22 

    for hour in range(start_hour, end_time + 1):
        start_datetime = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
        
        end_datetime_12h = start_datetime + timedelta(hours=12)

        available_rooms_12h_query = Room.objects.exclude(
            Q(booking__check_in__lt=end_datetime_12h) & Q(booking__check_out__gt=start_datetime)
        )
        

        available_rooms_12h.update(available_rooms_12h_query)

    return len(available_rooms_12h) 



def sample_sales_data(request):
    room_types_with_bookings = RoomType.objects.annotate(booking_count=Count('room__booking'))

    room_labels = []
    room_bookings = []
    room_sales = []

    room_types_with_bookings = RoomType.objects.annotate(
    booking_count=Count('room__booking'),
    total_sales=Sum('room__booking__total_amount')
    )

    for room_type in room_types_with_bookings:
        room_labels.append(room_type.room_type)
        room_bookings.append(room_type.booking_count)
        room_sales.append(room_type.total_sales if room_type.total_sales else 0)

    sales_months, sales_amounts = total_amount_per_month()
    bookCountperMonth = booking_count_per_month()
    sales_pastyearamounts = booking_count_per_month_past()

    total_bookings = Booking.objects.count() 
    guest_count = Guest.objects.count()

    now = datetime.now()
    current_month = now.month
    current_year = now.year

    monthSales = Booking.objects.filter(
        check_in__year=current_year,
        check_in__month=current_month
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    total_available_rooms = count_available_rooms()

    today = datetime.now()  

    this_year = today.year
    past_year = this_year - 1
    past_past_year = this_year - 2

    sales_labels = []
    if today.month <= 5:  
        sales_labels = [f"{past_year}-{this_year}", f"{past_past_year}-{past_year}"]
    else:
        sales_labels = [str(this_year), str(past_year)] 

    data = {
        'room_labels': room_labels,      
        'room_bookings': room_bookings, 
        'sales_months': sales_months, 
        'sales_amounts': sales_amounts,    
        'metric_total': total_bookings,
        'metric_guest': guest_count,
        'metric_month_sales': monthSales,
        'metric_avail_room': total_available_rooms,
        'sales_past_amounts': sales_pastyearamounts,
        'sales_labels': sales_labels,
        'bookCountperMonth':bookCountperMonth,
        'room_sales':room_sales,
    }
    
    return JsonResponse(data)


@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def option_room_view(request):
    return render(request, "dashboard/option-room.html")


def add_existing_room(request):
    rooms = Room.objects.all()
    roomtypes = RoomType.objects.all()

    if request.method == "POST":
        form = ExistingRoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.room_number = form.cleaned_data.get('room_number')
            room.room_type = form.cleaned_data.get('room_type')
            room.save()


            return render(request, "dashboard/room.html", {
                'rooms': rooms,
                'roomtypes': roomtypes,
                'form': ExistingRoomForm(),  
                'show_form': True  
            })
        else:
            return render(request, "dashboard/room.html", {
                'rooms': rooms,
                'roomtypes': roomtypes,
                'form': form,
                'show_form': False  
            })
    else:
        form = ExistingRoomForm()
        return render(request, "dashboard/room.html", {
            'rooms': rooms,
            'roomtypes': roomtypes,
            'form': form,
            'show_form': True  
        })