from django.core.mail import BadHeaderError
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.signals import valid_ipn_received
from datetime import timedelta, time, datetime
from .models import RoomType, Room, Guest, TempGuest, Booking
from users.models import CustomUser
from .forms import GuestForm, BookingForm, BookGuestForm
from .controllers import create_payment_link
from lac.utils.email_utils import send_email_contact
import uuid
import urllib.parse
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)
@csrf_exempt
def paypal_ipn(request):
    # Decode and log the raw IPN data for debugging purposes
    ipn_data = request.body.decode('utf-8')
    print("IPN Request Data:", ipn_data)
    logger.info(f"IPN Request Data: {ipn_data}")
    # Parse the IPN data into a dictionary
    parsed_data = dict(urllib.parse.parse_qsl(ipn_data))
    first_name = request.session.get('first_name', '')
    print("first name:", first_name)
    payment_status = parsed_data.get("payment_status", "")
    mc_gross = parsed_data.get("mc_gross", "")
    txn_id = parsed_data.get("txn_id", "")
    payer_email = parsed_data.get("payer_email", "")
    custom_value = parsed_data.get("custom", "") 
    print(f"Payment Status: {payment_status}")
    print(f"Amount: {mc_gross}")
    print(f"Transaction ID: {txn_id}")
    print(f"Payer Email: {payer_email}")
    print(f"Custom Value: {custom_value}")  
    custom_data = json.loads(custom_value)
    temp_guest = get_object_or_404(TempGuest, id=custom_data['tg'])
    room = get_object_or_404(Room, id=temp_guest.room)
    user_id = temp_guest.user
    if payment_status == "Completed":
        print("Payment completed successfully.")
        user = get_object_or_404(CustomUser, id=user_id)
        if Guest.objects.filter(user_id=user).exists():
            guest = get_object_or_404(Guest,user_id=user)
        else:
            new_guest = Guest(  
                first_name=temp_guest.first_name,
                last_name=temp_guest.last_name,
                address=temp_guest.address,
                phone=temp_guest.phone,
                user_id=user.id,
                date_of_birth=temp_guest.date_of_birth  
            )
            new_guest.save()
            guest = new_guest
        book = Booking(
            total_amount=temp_guest.total_amount,
            room=room,
            duration=temp_guest.duration,
            check_in=temp_guest.check_in,
            check_out=temp_guest.check_out,
            guest=guest,
            kid_count=temp_guest.kid_count,
            adult_count=temp_guest.adult_count,
            is_overnight=temp_guest.is_overnight
        )
        book.save()
        name =  "hoihoi"
        email = "camalig.j29@gmail.com"
        subject = "ewam"
        message = "hoy"
        if name and email and subject and message:
            try:
                result = send_email_contact(name, email, subject, message, 'camalig.j29@gmail.com', 'content/email_template.html')
                
                if result['success']:
                    return JsonResponse({"message": result['message']}) 
                else:
                     return JsonResponse({'error': result['error']}, status=500)             
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=400)
            
            except Exception as e:
                return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
        
        else:
            return JsonResponse({'error': 'Make sure all fields are entered and valid.'}, status=400)
    else:
        print("Payment not completed.")

    return HttpResponse(status=200)




def index(request):
    return render(request, "content/index.html")

def room_view(request):
    roomtypes = RoomType.objects.all()
    return render(request, "content/rooms.html", { 'roomtypes':roomtypes } )

def service_view(request):
    return render(request, "content/service.html")

@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                result = send_email_contact(name, email, subject, message, 'lacresortfarm@gmail.com', 'content/email_template.html')
                
                if result['success']:
                    return JsonResponse({"message": result['message']}) 
                else:
                     return JsonResponse({'error': result['error']}, status=500)             
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=400)
            
            except Exception as e:
                return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
        
        else:
            return JsonResponse({'error': 'Make sure all fields are entered and valid.'}, status=400)
    
    return render(request, 'content/contact.html')

def about_view(request):
    return render(request, "content/about.html")

@login_required(login_url="users:login")
def book_view1(request):
    roomtypes = RoomType.objects.all()
    return render(request, "content/booking.html", { 'roomtypes':roomtypes } )

def book_view2(request):
    # Retrieve session data
    first_name = request.session.get('first_name', '')
    last_name = request.session.get('last_name', '')
    address = request.session.get('address', '')
    phone = request.session.get('phone', '')
    date_of_birth = request.session.get('date_of_birth', '')
    check_in_date = request.session.get('check_in_date', '')
    check_out_date = request.session.get('check_out_date', '')
    check_out_time = request.session.get('check_out_time', '')
    kid_count = request.session.get('kid_count', '')
    adult_count = request.session.get('adult_count', '')
    check_in = request.session.get('check_in', '')
    check_in_datetime = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")

    check_in_time = check_in_datetime.time()
    start_time = time(14, 0)  
    end_time = time(22, 0)    # 8 PM
    
    check_out = request.session.get('check_out', '')
    room_id = request.session.get('room', '')
    total_amount = request.session.get('total_amount', '')
    duration = request.session.get('duration', '')
    email = request.session.get('email', '')
    user_id = request.user.id
    room = get_object_or_404(Room, id=room_id)
    check_in_formatted = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
    f_check_in = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
    f_check_out = f_check_in + timedelta(hours=int(duration))
    f_duration = timedelta(hours=int(duration))
        

    if start_time <= check_in_time <= end_time or int(duration) == 24:
        entrance_fee = (float(adult_count)*150) + (float(kid_count)*100)
        adult_price = 150
        kid_price = 100
        print("it is overnight")
        is_overnight = True
    else:
        entrance_fee = (float(adult_count)*100) + (float(kid_count)*50)
        adult_price = 100
        kid_price = 50  
        is_overnight = False
        print("its is not overnight")
    
    print(check_in_time)
    print(entrance_fee)
    room_price = room.room_type.price

    total_amount = float(room_price) + float(entrance_fee)
    total_amount = total_amount + float(200)
    print(total_amount)
    if room.room_type.is_cottage_required:
        cottage_price = 750
        is_cottage_required = True
        print("it is cottage required")
    else:
        cottage_price = 0
        is_cottage_required = False
        print("not")

    total_amount = float(total_amount) + float(cottage_price)
    

    temp_guest = TempGuest(  
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
        user=user_id,
        date_of_birth=date_of_birth,
        room=room_id,
        check_in=f_check_in,
        check_out=f_check_out,
        duration=f_duration,
        adult_count=adult_count,
        kid_count=kid_count,
        is_overnight=is_overnight,
        total_amount=total_amount,
    )
    temp_guest.save()
    check_out = check_in_formatted + timedelta(hours=int(duration))
    check_out = str(check_out)  
    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_amount,
        'item_name': "any",
        'invoice': str(uuid.uuid4()),
        'currency_code': 'PHP',
        'notify_url': "https://d310-2001-4453-6c4-6400-d52b-aa8c-4cae-1ecc.ngrok-free.app/paypal-ipn/",
        'return_url': f"http://{host}/booking/step4/{temp_guest.id}",
        'custom': json.dumps({
            'tg': str(temp_guest.id),
        })
    }



    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'phone': phone,
        'date_of_birth': date_of_birth,
        'check_in_date': check_in_date,
        'check_in_time': check_in_time,
        'check_out_date': check_out_date,
        'check_out_time': check_out_time,
        'check_in': check_in,
        'check_out': check_out,
        'room_id': room,
        'total_amount': total_amount,
        'duration': duration,
        'kid_count': kid_count,
        'adult_count': adult_count,
        'entrance_fee': entrance_fee,
        'room_price': room_price,
        'total_amount': total_amount,
        'kid_price': kid_price,
        'is_cottage_required': is_cottage_required,
        'adult_price': adult_price,
        'paypal': paypal_payment,
        
    }

    return render(request, "content/book_step2.html", context)





def book_view3(request):
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        room_id = request.POST.get('room_id')
        check_in_time = request.POST.get('check_in_time')
        request.session['check_in_time'] = check_in_time
        check_in_unformat = request.POST.get('check_in_date')
        duration = request.POST.get('duration')
        duration = int(duration)

        if check_in_unformat.startswith("Sept"):
            formatted_check_in_date = check_in_unformat.replace("Sept", "Sep")
        else:
            formatted_check_in_date = check_in_unformat
        date_object = datetime.strptime(formatted_check_in_date, '%b. %d, %Y')

        check_in_time = check_in_time.replace('.', '')
        
        check_in_date = date_object.strftime('%Y-%m-%d')
        request.session['check_in_date'] = str(check_in_date)
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
        
        check_in_time = datetime.strptime(check_in_time, '%I %p').time()
        check_in = datetime.combine(check_in_date, check_in_time)
        check_out = check_in + timedelta(hours=1)
        request.session['check_out'] = str(check_out)
        request.session['check_in'] = str(check_in)
        check_out = check_in + timedelta(hours=duration)
        
        check_out_date = check_out.date() 
        request.session['check_out_date'] = str(check_out_date)
        room = get_object_or_404(Room, id=room_id)
        email = request.user.email
        email = str(email)
        form = BookGuestForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = str(form.cleaned_data.get('first_name', ''))
            request.session['last_name'] = str(form.cleaned_data.get('last_name', ''))
            request.session['address'] = str(form.cleaned_data.get('address', ''))
            request.session['phone'] = str(form.cleaned_data.get('phone', ''))
            request.session['date_of_birth'] = str(form.cleaned_data.get('date_of_birth', ''))
            request.session['email'] = email
            request.session['adult_count'] = str(form.cleaned_data.get('adult_count', ''))
            request.session['kid_count'] = str(form.cleaned_data.get('kid_count', ''))
            request.session['check_out'] = check_out.strftime('%Y-%m-%d') if check_out else None

            room_id = request.POST.get('room_id')
            print(room_id)
            room = get_object_or_404(Room, id=room_id)

            request.session['room'] = str(room.id) 
            request.session['total_amount'] = str(room.room_type.price) 
            request.session['duration'] = str(duration)
            print("line 318") 
            return redirect('content:book_2')

        else:
            check_in_date = check_in_date.date()
            check_out_time = check_out.time()
            print("else in the form valid")
            print(form.errors)  
            return render(request, "content/book_step3.html", {
                "form": form,
                "check_in": check_in,
                "room": room,
                "email": email,
                'check_in_date': check_in_date,
                'check_out_date': check_out_date,
                'check_in_time': check_in_time,
                'check_out_time': check_out_time,
                'duration': duration
            })
    elif 'back' in request.GET and request.GET.get('back') == 'true':
        address = request.session.get('address', '')  
        first_name = request.session.get('first_name', '')  
        last_name = request.session.get('last_name', '')  
        date_of_birth = request.session.get('date_of_birth', '')  
        phone = request.session.get('phone', '')  
        adult_count = request.session.get('adult_count', '')  
        kid_count = request.session.get('kid_count', '')  
        duration = request.session.get('duration', '') 
        check_in_time = request.session.get('check_in_time', '')
        room_id = request.session.get('room', '')
        room = get_object_or_404(Room,id=room_id)
        print("this is room:", room_id)
        
        check_in_date = request.session.get('check_in_date', '') 
        date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
        f_check_in_date = date_obj.strftime("%b. %d, %Y") 
        
        time_var = check_in_time.replace(".", "") 
        time_var = datetime.strptime(time_var, "%I %p").time()
        date_var = datetime.strptime(check_in_date, "%Y-%m-%d").date()  

        check_in_var = datetime.combine(date_var, time_var)  
        check_out_var = check_in_var + timedelta(hours=int(duration)) 
        
        check_out_date = check_out_var.date()
        check_out_time = check_out_var.time()
        print("check_in",check_in_var)
        email = request.user.email
        print('check_out', check_out_var)
        context = {
            'address': address,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'phone': phone,
            'email': email,
            'kid_count': kid_count,
            'adult_count': adult_count,
            'duration': duration,
            'check_in_date': f_check_in_date,
            'check_in_time': check_in_time,
            'check_out_date': check_out_date,
            'check_out_time': check_out_time,
            'room': room,
        }
        print('address:', address)
        return render(request, 'content/book_step3.html', context)
    else:
        check_in_unformat = request.GET.get('book_check_in_date')
        check_in_time = request.GET.get("book_check_in_time")
        duration = request.GET.get('book_duration')
        duration = int(duration)
        date_object = datetime.strptime(check_in_unformat, '%b. %d, %Y')
        check_in_date = date_object.strftime('%Y-%m-%d')
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date() if check_in_date else None
        print("else in request method")
        start_time = datetime.strptime(check_in_time, '%I:%M %p').time() 
        start_datetime = datetime.combine(check_in_date, start_time)
        end_datetime = start_datetime + timedelta(hours=duration)

        check_out_date = end_datetime.date()
        check_out_time = end_datetime.time()
        check_in_time = start_datetime.time()

        room_id = request.GET.get('roomtype')
        room = get_object_or_404(Room, id=room_id)
        email = request.user.email
        form = GuestForm()  
        
        context = {
            'form': form,
            'duration': duration,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'check_in_time': check_in_time,
            'check_out_time': check_out_time,
            'room': room,
            'email': email,
        }

        return render(request, 'content/book_step3.html', context)


def book_view4(request, temp_id):
    details = get_object_or_404(TempGuest,id=temp_id)
    room = get_object_or_404(Room, id=details.room)
    email = request.user.email
    context = {
        "email":email,
        "details":details,
        "room":room
    }
    return render(request, "content/book_step4.html", context)

@login_required(login_url="users:login")
def calendar_view(request):
    fullyBookDates = getFullyBookDates()
    print(fullyBookDates)
    context = {
        "fullBookDates": fullyBookDates
    }
    return render(request, "content/calendar.html", context)


from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

def getFullyBookDates():
    now = timezone.localtime(timezone.now())
    
    if now.minute > 0:
        start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        start_time = now
    
    target_end_time = start_time.replace(hour=22, minute=0, second=0, microsecond=0)
    target_end_date = (start_time + timedelta(days=365)).replace(hour=22, minute=0, second=0, microsecond=0)

    start_date = start_time
    initial_date = start_date

    fully_booked_dates = []

    while start_date <= target_end_date:    
        if start_date != initial_date:
            loop_start_time = start_date.replace(hour=8, minute=0, second=0, microsecond=0)
        else:
            loop_start_time = start_date
            condition_time = loop_start_time.time()
            eight_am = time(8, 0) 
            if condition_time < eight_am:
                loop_start_time = start_date.replace(hour=8, minute=0, second=0, microsecond=0)
            else:
                loop_start_time = start_date
        
        loop_end_time = loop_start_time.replace(hour=22, minute=0, second=0, microsecond=0)

        check_count = 0
        while loop_start_time <= loop_end_time:
            rooms = Room.objects.all()
            end_datetime = loop_start_time + timedelta(hours=12)

            booked_rooms = Booking.objects.filter(
                Q(check_in__lt=end_datetime) & Q(check_out__gt=loop_start_time) & Q(status="Booked")
            ).values_list('room', flat=True)
            available_rooms = rooms.exclude(id__in=booked_rooms)

            print(f"Current start_time: {loop_start_time}, end_datetime: {end_datetime}")
            print(f"Available rooms for {loop_start_time}: {available_rooms}")


            if available_rooms.count() != 0:
                check_count += 1
            loop_start_time += timedelta(hours=1)
        
        if check_count == 0:
            fully_booked_dates.append(loop_start_time.date().strftime('%Y-%m-%d')) 

        start_date += timedelta(days=1)
    
    return fully_booked_dates

def search_room(request):
    if request.method == 'GET':
        # Get and format the check-in date
        check_in_unformat = request.GET.get('check_in_date')
        try:
            date_object = datetime.strptime(check_in_unformat, '%b. %d, %Y')
            check_in_date = date_object.date()  # Convert to date object
        except (ValueError, TypeError):
            return render(request, 'content/booking.html', {'error': 'Invalid check-in date format.'})

        # Get other parameters
        capacity = request.GET.get("capacity", 1)
        try:
            capacity = int(capacity)
        except ValueError:
            capacity = 1  # Default to 1 if invalid

        checkin_time = request.GET.get("checkin_time", "12:00")
        try:
            start_time = datetime.strptime(checkin_time, '%H:%M').time()
        except ValueError:
            return render(request, 'content/booking.html', {'error': 'Invalid check-in time format.'})

        duration = request.GET.get("duration", 8)
        try:
            duration = int(duration)
        except ValueError:
            duration = 8  # Default to 8 hours if invalid

        # Compute start and end datetime
        start_datetime = datetime.combine(check_in_date, start_time)
        end_datetime = start_datetime + timedelta(hours=duration)

        # Filter rooms by capacity
        rooms = Room.objects.filter(room_type__capacity__gte=capacity)

        # Filter out booked rooms during the specified time range
        booked_rooms = Booking.objects.filter(
            Q(check_in__lt=end_datetime) & Q(check_out__gt=start_datetime) & Q(status="Booked")
        ).values_list('room', flat=True)

        # Exclude booked rooms
        available_rooms = rooms.exclude(id__in=booked_rooms)

        # Optional debug outputs
        print("Start Time:", start_datetime)
        print("End Time:", end_datetime)
        print("Available Rooms:", available_rooms)

        # Format check-in date for the template
        check_in_date_str = date_object.strftime('%b. %d, %Y')

        # Context for the template
        context = {
            'rooms': available_rooms.distinct('room_type'),  # Ensure unique room types
            'capacity': capacity,
            'check_in_date': check_in_date_str,
            'duration': duration,
            'checkin_time': checkin_time
        }

        return render(request, 'content/booking.html', context)

def initial_search(request):
    if request.method == "GET":
        print("call initial")
        check_in_date = request.GET.get('check_in', None) 
        date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
        str_check_in = date_obj.strftime("%b. %d, %Y")
        print("check_in", check_in_date)

        available_times = get_time(check_in_date)
        initial_time = available_times[0]
        available_times = {
            time: datetime.strptime(time, "%I:%M %p").strftime("%H:%M")
            for time in available_times
        }
        

        date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
        initial_time = datetime.strptime(initial_time, "%I:%M %p").time()
        time_str = initial_time.strftime("%I:%M %p")
        capacity = 1
        check_in = datetime.combine(date_obj, initial_time)
        print(check_in)

        rooms = get_rooms(check_in, capacity)
        print(rooms)

        context = {
            'str_check_in': str_check_in,
            'check_in_date': check_in_date,
            'initial_time': time_str,
            'available_times': available_times,
            'rooms': rooms
        }
        return render(request, 'content/booking.html', context)


def get_time(check_in_date):
    selected_date = check_in_date
    if selected_date:
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
        current_time = datetime.now()
        if current_time.date() == selected_date_obj.date():
            if current_time.time() < time(8, 0):
                current_time = current_time.replace(hour=8, minute=0, second=0, microsecond=0)
                start_datetime = current_time
            elif current_time.time() > selected_date_obj.time():
                start_datetime = selected_date_obj.replace(hour=(current_time.hour + 1) % 24, minute=0, second=0)
            else:
                start_datetime = selected_date_obj.replace(hour=current_time.hour, minute=current_time.minute, second=0)
        else:
            start_datetime = selected_date_obj.replace(hour=8, minute=0, second=0)
            
        end_datetime = start_datetime.replace(hour=22, minute=0, second=0, microsecond=0)
        
        available_times = []

        while start_datetime <= end_datetime:
                rooms = Room.objects.all()
                
                booked_rooms = Booking.objects.filter(
                Q(check_in__lt=end_datetime) & Q(check_out__gt=start_datetime) & Q(status="Booked")
                ).values_list('room', flat=True)
                available_rooms = rooms.exclude(id__in=booked_rooms)

                if available_rooms.count() != 0:
                    available_times.append(start_datetime.strftime("%I:%M %p"))
                start_datetime += timedelta(hours=1)  
        
        return available_times
    
def get_rooms(check_in, capacity, duration=None):
        if duration:
            duration = duration
        else:
            duration = 12
        start_datetime = check_in
        end_datetime = check_in + timedelta(hours=duration)

        rooms = Room.objects.filter(room_type__capacity__gte=capacity)

        booked_rooms = Booking.objects.filter(
            Q(check_in__lt=end_datetime) & Q(check_out__gt=start_datetime) & Q(status="Booked")
        ).values_list('room', flat=True)

        available_rooms = rooms.exclude(id__in=booked_rooms)
        filtered_rooms = available_rooms.distinct('room_type')
        return filtered_rooms

def get_dynamic_rooms(check_in, capacity, duration):
        duration = duration
        start_datetime = check_in
        end_datetime = check_in + timedelta(hours=duration)

        rooms = Room.objects.filter(room_type__capacity__gte=capacity)

        booked_rooms = Booking.objects.filter(
            Q(check_in__lt=end_datetime) & Q(check_out__gt=start_datetime) & Q(status="Booked")
        ).values_list('room', flat=True)

        available_rooms = rooms.exclude(id__in=booked_rooms)
        available_rooms = available_rooms.distinct('room_type')
        return available_rooms

def dynamic_search(request):
    try:
        checkin_date_str = request.GET.get('checkin_date')
        duration = request.GET.get('duration')
        checkin_time_str = request.GET.get('checkin_time')
        capacity = request.GET.get('capacity')

        checkin_date = datetime.strptime(checkin_date_str, "%b. %d, %Y")
        checkin_time = datetime.strptime(checkin_time_str, "%H:%M").time()
        check_in = datetime.combine(checkin_date, checkin_time)

        rooms = get_rooms(check_in, capacity, int(duration))
        rooms_data = [{'id': room.id, 'name': room.room_number, 'capacity': room.room_type.capacity, 'picture_url': room.room_type.picture.url, 'price': room.room_type.price, 'description': room.room_type.description, 'roomtype': room.room_type.room_type} for room in rooms]

        return JsonResponse({'rooms': rooms_data, 'checkin_date': checkin_date,
        'duration': duration,
        'checkin_time': checkin_time,
        'capacity': capacity,
        'check_in':check_in})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)