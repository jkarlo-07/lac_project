from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from content.models import Booking, Room, Guest, RoomType
from django.http import JsonResponse
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
    booking_counts = [0] * 6  # Initialize booking counts with zeros for each of the last six months

    # Get the last six months from today, adding each month name to the list
    for i in range(6):
        month_date = today - timedelta(days=30 * i)
        last_six_months.append(month_date.strftime('%B'))

    # Reverse last_six_months to display in chronological order
    last_six_months.reverse()
    booking_counts.reverse()

    # Filter bookings within the last six months
    bookings = Booking.objects.filter(check_in__gte=today - timedelta(days=180))

    # Count bookings for each month
    for booking in bookings:
        month = booking.check_in.strftime('%B')
        if month in last_six_months:
            index = last_six_months.index(month)
            booking_counts[index] += 1  # Increment count for the month

    return last_six_months, booking_counts

def booking_count_per_month_past():
    today = datetime.now()

    # Generate labels for the last six months (from last year)
    last_six_months = []
    booking_counts = [0] * 6

    for i in range(5, -1, -1):  # Start from the oldest month and move to the most recent
        month_date = today.replace(year=today.year - 1) - relativedelta(months=i)
        last_six_months.append(month_date.strftime('%B %Y'))

    # Filter bookings for the last six months of last year
    bookings = Booking.objects.filter(
        check_in__year=today.year - 1,
        check_in__month__in=[datetime.strptime(month, '%B %Y').month for month in last_six_months]
    )

    # Count bookings per month
    for booking in bookings:
        month_year = booking.check_in.strftime('%B %Y')
        if month_year in last_six_months:
            index = last_six_months.index(month_year)
            booking_counts[index] += 1  # Increment count for the corresponding month

    return booking_counts


from django.db.models import Q
from datetime import datetime, timedelta

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

    for room_type in room_types_with_bookings:
        room_labels.append(room_type.room_type)
        room_bookings.append(room_type.booking_count)

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
    }
    
    return JsonResponse(data)


@login_required(login_url="users:login")
@user_passes_test(is_staff, login_url="content:index") 
def option_room_view(request):
    return render(request, "dashboard/option-room.html")