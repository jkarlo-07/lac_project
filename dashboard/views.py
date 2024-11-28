from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from content.models import Booking, Room, Guest, RoomType, FullyBookedDates
from django.http import JsonResponse
from django.db.models import Count, Sum
from datetime import datetime, timedelta, time, date
from dateutil.relativedelta import relativedelta
from .forms import ExistingRoomForm, NewRoomTypeForm, UpdateRoomTypeForm, UpdateGuestForm, UpdateBookingForm, AddBookingForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from decimal import Decimal


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
        month_date = today - relativedelta(months=i)
        last_six_months.append(month_date.strftime('%B')) 
        total_amounts.append(0)  

    six_months_ago = today - relativedelta(months=6)
    bookings = Booking.objects.filter(check_in__gte=six_months_ago)

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
        month_date = today - relativedelta(months=i)
        last_six_months.append(month_date.strftime('%B'))  

    last_six_months.reverse()
    booking_counts.reverse()

    six_months_ago = today - relativedelta(months=6)
    bookings = Booking.objects.filter(check_in__gte=six_months_ago)

    for booking in bookings:
        month = booking.check_in.strftime('%B')
        if month in last_six_months:
            index = last_six_months.index(month)
            booking_counts[index] += 1

    return last_six_months, booking_counts

def booking_count_per_month_past(past_year):
    today = datetime.now()

    last_six_months = []
    booking_counts = [0] * 6

    for i in range(5, -1, -1):  
        month_date = today.replace(year=today.year - past_year) - relativedelta(months=i)
        last_six_months.append(month_date.strftime('%B %Y'))

    bookings = Booking.objects.filter(
        check_in__year=today.year - past_year,
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
    sales_pastyearamounts = booking_count_per_month_past(1)
    sales_past2yearamounts = booking_count_per_month_past(2)

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
    past_3_years = this_year - 3

    sales_labels = []
    if today.month <= 5:  
        sales_labels = [f"{past_year}-{this_year}", f"{past_past_year}-{past_year}", f"{past_3_years}-{past_past_year}"]
    else:
        sales_labels = [str(this_year), str(past_year), past_past_year] 

    sales_labels.append("2022")
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
        'sales_past2_amounts': sales_past2yearamounts,
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
            room_type_post = request.POST.get('room_type')
            roomtype = get_object_or_404(RoomType, id=room_type_post)
            room.room_type = roomtype
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
    

from django.db import transaction
from django.shortcuts import render

def add_new_room_type(request):
    rooms = Room.objects.all()
    roomtypes = RoomType.objects.all()

    if request.method == 'POST':
        form = NewRoomTypeForm(request.POST, request.FILES)
        form2 = ExistingRoomForm(request.POST)

        if form.is_valid() and form2.is_valid():
            roomtype = form.save(commit=False)  

            is_cottage_required = request.POST.get('cottage_req')
            if is_cottage_required == "on":
                roomtype.is_cottage_required = True
            else:
                roomtype.is_cottage_required = False
            roomtype.base_price = form.cleaned_data.get('price')
            roomtype.room_type = form.cleaned_data.get('room_type')
            roomtype.description = form.cleaned_data.get('description')
            roomtype.price = form.cleaned_data.get('price')
            roomtype.capacity = form.cleaned_data.get('capacity')
            roomtype.picture = form.cleaned_data.get('picture')

            with transaction.atomic():
                roomtype.save() 

                room = form2.save(commit=False)
                room.room_type = roomtype
                room.room_number = form2.cleaned_data.get('room_number')
                room.save() 

                form = NewRoomTypeForm()
                form2 = ExistingRoomForm()

        else:
            if not form.is_valid():
                print('Form errors:', form.errors)
            if not form2.is_valid():
                print('Form2 errors:', form2.errors)

            return render(request, "dashboard/room.html", {
                'rooms': rooms,
                'roomtypes': roomtypes,
                'form': form,
                'form2': form2,
                'show_form': True,
                'show_form2': True  
            })

    else:
        form = NewRoomTypeForm()
        form2 = ExistingRoomForm()

    return render(request, "dashboard/room.html", {
        'rooms': rooms,
        'roomtypes': roomtypes,
        'form': form,
        'form2': form2,
        'show_form': True,
        'show_form2': False
    })
    
from django.http import JsonResponse
from django.template.loader import render_to_string

def fetch_all_rooms(request):
    rooms = Room.objects.all()
    roomtypes = RoomType.objects.all()
    switch_to_room = request.GET.get('switchToRoom') == 'true'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_content = render_to_string(
            'dashboard/room_table.html' if not switch_to_room else 'dashboard/room_type_table.html',
            {'rooms': rooms, 'roomtypes': roomtypes}
        )
        return JsonResponse({'html': html_content})
    
    return render(request, "dashboard/room.html", {
        'rooms': rooms, 
        'roomtypes': roomtypes, 
        'switchToRoom': switch_to_room,
    })

def delete_room(request):
    if request.method == "POST":
        room_id = request.POST.get('deleteID')
        
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        
        rooms = Room.objects.all()
        roomtypes = RoomType.objects.all()
        return render(request, "dashboard/room.html", {'rooms': rooms, 'roomtypes': roomtypes, 'show_form': True  })


    return redirect('home')

def delete_roomtype(request):
    if request.method == "POST":
        room_id = request.POST.get('deleteID2')
        room = get_object_or_404(RoomType, id=room_id)
        room.delete()
        
        rooms = Room.objects.all()
        roomtypes = RoomType.objects.all()
        switch_to_room = request.GET.get('switchToRoom') == 'true'

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html_content = render_to_string(
                'dashboard/room_table.html' if not switch_to_room else 'dashboard/room_type_table.html',
                {'rooms': rooms, 'roomtypes': roomtypes}
            )
            return JsonResponse({'html': html_content})
        
        return render(request, "dashboard/room.html", {'rooms': rooms, 'roomtypes': roomtypes, 'show_form': True, 'switchToRoom': "true",  })


    return redirect('home')

def update_room(request):
    if request.method == "POST":
        room_id = request.POST.get('room_id')
        updated_room = request.POST.get('room_number')
        updated_roomtype = request.POST.get('room_type')
        roomtype = get_object_or_404(RoomType, id=updated_roomtype)
        room = get_object_or_404(Room, id=room_id)
        room.room_number = updated_room
        room.room_type = roomtype
        room.save()

        rooms = Room.objects.all()
        roomtypes = RoomType.objects.all()
        switch_to_room = request.GET.get('switchToRoom') == 'false'

        return render(request, "dashboard/room.html", {'rooms': rooms, 'roomtypes': roomtypes, 'show_form': True  })
    
def update_room_type(request):
    if request.method == 'POST':
        form = UpdateRoomTypeForm(request.POST, request.FILES)
        if form.is_valid():
            roomtype_id = request.POST.get("roomtype_id")
            room_type = form.cleaned_data.get('room_type', '')
            price = form.cleaned_data.get('price', '')
            description = form.cleaned_data.get('description', '')
            capacity = form.cleaned_data.get('capacity', '')
            is_cottage_required = form.cleaned_data.get('is_cottage_required', '')
            
                
            roomtype_model = get_object_or_404(RoomType,id=roomtype_id)
            roomtype_model.room_type = room_type
            roomtype_model.price = price
            roomtype_model.description = description
            roomtype_model.base_price = price
            roomtype_model.capacity = capacity
            if is_cottage_required == "on":
                roomtype_model.is_cottage_required = True
            else:
                roomtype_model.is_cottage_required = False
                
            roomtype_model.picture = form.cleaned_data.get('picture')
            if form.cleaned_data.get('picture'):
                roomtype_model.save(update_fields=['room_type', 'price', 'description', 'base_price', 'capacity', 'is_cottage_required', 'picture'])
            else:
                roomtype_model.save(update_fields=['room_type', 'price', 'description', 'base_price', 'capacity', 'is_cottage_required'])


            rooms = Room.objects.all()
            roomtypes = RoomType.objects.all()
            switch_to_room = request.GET.get('switchToRoom') == 'true'

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html_content = render_to_string(
                    'dashboard/room_table.html' if not switch_to_room else 'dashboard/room_type_table.html',
                    {'rooms': rooms, 'roomtypes': roomtypes}
                )
                return JsonResponse({'html': html_content})
            form = UpdateRoomTypeForm()
            return render(request, "dashboard/room.html", 
                          {'rooms': rooms, 
                           'roomtypes': roomtypes, 
                           'show_form': True, 
                           'switchToRoom': "true", 
                           "showUpdateType": False})
        else:
            rooms = Room.objects.all()
            roomtypes = RoomType.objects.all()
            switch_to_room = request.GET.get('switchToRoom') == 'true'

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html_content = render_to_string(
                    'dashboard/room_table.html' if not switch_to_room else 'dashboard/room_type_table.html',
                    {'rooms': rooms, 'roomtypes': roomtypes}
                )
                return JsonResponse({'html': html_content})
            
            return render(request, "dashboard/room.html", 
                          {'rooms': rooms, 
                           'roomtypes': roomtypes, 
                           'show_form': True, 
                           'switchToRoom': "true", 
                           "showUpdateType": True,
                           "form": form,
                           "room_id":request.POST.get("roomtype_id")}
                           )

def delete_guest(request):
    if request.method == "POST":
        guest_id = request.POST.get('deleteID')
        guest = get_object_or_404(Guest,id=guest_id)
        guest.delete()
        guests = Guest.objects.all()
        return redirect("dashboard:guest")
    else:
        return redirect("content:index")
    
def update_guest(request):
    if request.method == "POST":
        guest_id = request.POST.get('id')
        guest = get_object_or_404(Guest, id=guest_id)
        form = UpdateGuestForm(request.POST)
        guests = Guest.objects.all()
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            address = form.cleaned_data.get('address', '')
            date_of_birth = form.cleaned_data.get('date_of_birth', '')
            phone = form.cleaned_data.get('phone', '')
            guest.first_name = first_name
            guest.last_name = last_name
            guest.address = address
            guest.date_of_birth = date_of_birth
            guest.phone = phone
            guest.save(update_fields=['first_name', 'last_name', 'address', 'date_of_birth','phone'])
            return redirect("dashboard:guest")
        else:
            return render(request, "dashboard/guest.html", {'guests' : guests, 'form': form, 'show_form': True, 'id':guest_id})
        
def delete_booking(request):
    bookings = Booking.objects.all().order_by('-check_in')
    if request.method == 'POST':
        book_id = request.POST.get('deleteID')
        book_record = get_object_or_404(Booking, id=book_id)
        checkin_date = book_record.check_in.date()
        book_record.delete()
        check_remove_fullbook(checkin_date)
        return render(request, "dashboard/booking.html", {'booking': bookings})

def get_time(request):
    selected_date = request.GET.get('date')

    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, "%m/%d/%Y")
            current_time = datetime.now()

            if current_time.date() == selected_date_obj.date():
                if current_time.time() > selected_date_obj.time():
                    start_datetime = selected_date_obj.replace(hour=(current_time.hour + 1) % 24, minute=0, second=0)
                else:
                    start_datetime = selected_date_obj.replace(hour=current_time.hour, minute=current_time.minute, second=0)
            else:
                start_datetime = selected_date_obj.replace(hour=8, minute=0, second=0)
            
            end_datetime = start_datetime.replace(hour=22, minute=0, second=0, microsecond=0)


            available_times = []
            while start_datetime <= end_datetime:
                rooms = Room.objects.all()
                loop_end_datetime = start_datetime + timedelta(hours=12)
                booked_rooms = Booking.objects.filter(
                Q(check_in__lt=loop_end_datetime) & Q(check_out__gt=start_datetime) & Q(status="Booked")
                ).values_list('room', flat=True)
                available_rooms = rooms.exclude(id__in=booked_rooms)

                if available_rooms.count() != 0:
                    available_times.append(start_datetime.strftime("%I:%M %p"))
                start_datetime += timedelta(hours=1)  

            return JsonResponse({'available_times': available_times})

        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

    return JsonResponse({'error': 'No date provided'}, status=400)

def get_rooms(request):
    selected_date = request.GET.get('date')
    selected_time = request.GET.get('time')
    duration = request.GET.get('duration')
    if selected_date and selected_time:
        try:
            combined_datetime_str = f"{selected_date} {selected_time}"
            
            start_datetime = datetime.strptime(combined_datetime_str, "%m/%d/%Y %I:%M %p")
            duration_hours = int(duration) if duration else 0
            end_datetime = start_datetime + timedelta(hours=duration_hours)
            
            rooms = Room.objects.all()
            booked_rooms = Booking.objects.filter(
                Q(check_in__lt=end_datetime) & Q(check_out__gt=start_datetime) & Q(status="Booked")
            ).values_list('room', flat=True)
            available_rooms = rooms.exclude(id__in=booked_rooms)
            available_rooms = available_rooms.distinct('room_type')

            available_rooms_array = []

            for room in available_rooms:
                available_rooms_array.append({
                    'room_type': room.room_type.room_type,  # Assuming 'room_type' is a related model
                    'room_id': room.id
                })


            
            data = {
                'combined_datetime': start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'available_rooms': available_rooms_array
            }
            return JsonResponse(data)
        except ValueError as e:
            return JsonResponse({'error': f"Error parsing date/time: {e}"}, status=400)
    else:
        return JsonResponse({'error': 'Date and time are required!'}, status=400)
    
def update_booking(request):
    if request.method == "POST":
        book_id = request.POST.get('id')
        booking = get_object_or_404(Booking, id=book_id)
        past_checkin_date = booking.check_in.date()
        form = UpdateBookingForm(request.POST)
        bookings = Booking.objects.all().order_by('-check_in')
        if form.is_valid():
            kid_count = form.cleaned_data["kid_count"]
            adult_count = form.cleaned_data["adult_count"]

            checkin_date = request.POST.get("checkin_date")
            checkin_time = request.POST.get("checkin_time")
            duration = request.POST.get("duration")
            room = request.POST.get("room")
            room = get_object_or_404(Room, id=room)
            datetime_str = f"{checkin_date} {checkin_time}"
            check_in = datetime.strptime(datetime_str, "%m/%d/%Y %I:%M %p")
            check_out = check_in + timedelta(hours=int(duration))

            total = room.room_type.price
            # Total price calculation
            if room.room_type.is_cottage_required:
                total += room.room_type.cottage_price
            
            start_time = time(14, 0)  
            end_time = time(22, 0) 
            check_in_time = check_in.time()

            if start_time <= check_in_time <= end_time or int(duration) == 24:
                entrance_fee = (Decimal(adult_count)*150) + (Decimal(kid_count)*100)
                is_overnight = True
            else:
                entrance_fee = (Decimal(adult_count)*100) + (Decimal(kid_count)*50)
                is_overnight = False

            total += entrance_fee
            booking.total_amount = float(total)
            booking.is_overnight = is_overnight
            booking.check_in = check_in
            booking.check_out = check_out
            booking.duration = timedelta(hours=int(duration)) 
            booking.room = room
            booking.adult_count = int(adult_count)
            booking.kid_count = int(kid_count)
            booking.save(update_fields=['check_in', 'check_out', 'duration', 'room','kid_count', 'adult_count', 'is_overnight', 'total_amount'])
            check_add_fullbook(check_in.date())
            check_remove_fullbook(past_checkin_date)
            

            return redirect("dashboard:booking")
        else:
            return render(request, "dashboard/booking.html", {'booking': bookings, 'show_form': True, 'form': form,'id': book_id, 'book': booking})
        

def add_booking(request):
    if request.method == 'POST':
        bookings = Booking.objects.all().order_by('-check_in')
        form = AddBookingForm(request.POST)
        if form.is_valid():
            guest = Guest(  
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                address=form.cleaned_data.get('address'),
                phone=form.cleaned_data.get('phone'),
                user_id=None,
                date_of_birth=form.cleaned_data.get('dob')  
            )
            guest.save()
            room = get_object_or_404(Room, pk=form.cleaned_data.get('room'))
            
            datetime_str = f"{form.cleaned_data.get('checkin_date')} {form.cleaned_data.get('checkin_time')}"
            check_in = datetime.strptime(datetime_str, "%m/%d/%Y %I:%M %p")
            check_out = check_in + timedelta(hours=int(form.cleaned_data.get('duration')))
            duration = form.cleaned_data.get('duration')
            adult_count = form.cleaned_data.get('adult_count')
            kid_count = form.cleaned_data.get('kid_count')

            start_time = time(14, 0)  
            end_time = time(22, 0) 
            check_in_time = check_in.time()


            if start_time <= check_in_time <= end_time or int(duration) == 24:
                entrance_fee = (Decimal(adult_count)*150) + (Decimal(kid_count)*100)
                is_overnight = True
            else:
                entrance_fee = (Decimal(adult_count)*100) + (Decimal(kid_count)*50)
                is_overnight = False
            total = room.room_type.price
            total += entrance_fee

            book = Booking(
                guest=guest,
                room=room,
                check_in=check_in,
                check_out=check_out,
                duration=timedelta(hours=int(duration)),
                adult_count=form.cleaned_data.get('adult_count'),
                kid_count=form.cleaned_data.get('kid_count'),
                is_overnight=is_overnight,
                total_amount=float(total),
                booking_created_at=datetime.now(),
            )
            
            book.save()
            checkin_date = check_in.date()
            check_add_fullbook(checkin_date)

            form = AddBookingForm()
            return redirect("dashboard:booking")
        else:
            return render(request, "dashboard/booking.html", {'booking': bookings, 'show_add_form': True, 'form': form})
    
    return render(request, "dashboard/booking.html", {'booking': bookings, 'show_add_form': False, 'form': form})

def check_add_fullbook(checkin_date):
    if checkin_date == datetime.now().date():
        current_time = datetime.now()
        if current_time.minute != 0:
            start_time = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        else:
            start_time = current_time
    else:
        start_time = datetime.combine(checkin_date, time(8, 0))
    
    end_time = datetime.combine(checkin_date, time(22, 0))

    check_count = 0
    while start_time <= end_time:
        rooms = Room.objects.all()
        print(start_time)
        loop_end_datetime = start_time + timedelta(hours=12)
        booked_rooms = Booking.objects.filter(
            Q(check_in__lt=loop_end_datetime) & Q(check_out__gt=start_time) & Q(status="Booked")
        ).values_list('room', flat=True)
        available_rooms = rooms.exclude(id__in=booked_rooms)

        print(f"Current start_time: {start_time}, end_datetime: {end_time}")
        print(f"Available rooms for {start_time}: {available_rooms}")


        if available_rooms.count() != 0:
                check_count += 1
            
        start_time += timedelta(hours=1)
        
    print(check_count)

    print("it is not now", check_count)
    if check_count == 0:
            fullybook = FullyBookedDates(date=checkin_date)
            fullybook.save()


def check_remove_fullbook(checkin_date):
    if checkin_date == datetime.now().date():
        current_time = datetime.now()
        if current_time.minute != 0:
            start_time = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        else:
            start_time = current_time
    else:
        start_time = datetime.combine(checkin_date, time(8, 0))
    
    end_time = datetime.combine(checkin_date, time(22, 0))

    check_count = 0
    while start_time <= end_time:
        rooms = Room.objects.all()
        print(start_time)
        loop_end_datetime = start_time + timedelta(hours=12)
        booked_rooms = Booking.objects.filter(
            Q(check_in__lt=loop_end_datetime) & Q(check_out__gt=start_time) & Q(status="Booked")
        ).values_list('room', flat=True)
        available_rooms = rooms.exclude(id__in=booked_rooms)

        print(f"Current start_time: {start_time}, end_datetime: {end_time}")
        print(f"Available rooms for {start_time}: {available_rooms}")


        if available_rooms.count() != 0:
                check_count += 1
            
        start_time += timedelta(hours=1)
        
    print(check_count)

    print("it is not now", check_count)
    if check_count != 0:
        is_date_exist = FullyBookedDates.objects.filter(date=checkin_date).exists()
        if is_date_exist:
            fullbook = FullyBookedDates.objects.get(date=checkin_date)
            fullbook.delete()
        else:
            print("The date does not exist.")

def change_booking_status(request):
    if request.method == 'POST':
        book_id = request.POST.get('id')
        book_record = get_object_or_404(Booking, id=book_id)
        checkin_date = book_record.check_in.date()
        if book_record.status == "Booked":
            book_record.status = "Canceled"
            book_record.save(update_fields=['status'])
            check_remove_fullbook(checkin_date)
        else:
            book_record.status = "Booked"
            book_record.save(update_fields=['status'])
            check_add_fullbook(checkin_date)
        
        return redirect('dashboard:booking')