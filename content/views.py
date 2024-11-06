from django.core.mail import BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import RoomType
from lac.utils.email_utils import send_email_contact
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import GuestForm, BookingForm
from datetime import timedelta, time, datetime
from .controllers import create_payment_link
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .models import RoomType, Room # Corrected to RoomType, as that is what you want to create
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.models import PayPalIPN
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import urllib.parse

@csrf_exempt
def paypal_ipn(request):
    # Decode and log the raw IPN data for debugging purposes
    ipn_data = request.body.decode('utf-8')
    print("IPN Request Data:", ipn_data)

    # Parse the IPN data into a dictionary
    parsed_data = dict(urllib.parse.parse_qsl(ipn_data))
    
    # Retrieve payment status and other important fields
    payment_status = parsed_data.get("payment_status", "")
    mc_gross = parsed_data.get("mc_gross", "")
    txn_id = parsed_data.get("txn_id", "")
    payer_email = parsed_data.get("payer_email", "")
    custom_value = parsed_data.get("custom", "")  # Get the 'custom' field

    # Log payment information
    print(f"Payment Status: {payment_status}")
    print(f"Amount: {mc_gross}")
    print(f"Transaction ID: {txn_id}")
    print(f"Payer Email: {payer_email}")
    print(f"Custom Value: {custom_value}")  # Log the custom value

    # Check if payment was completed successfully
    if payment_status == "Completed":
        print("Payment completed successfully.")
        # Add further logic, like updating your database with the payment status
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
    return render(request, "content/book_step2.html")

def book_view3(request):
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        room_id = request.POST.get('room_id')
        check_in_time = request.POST.get('check_in_time')
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
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_in_time = datetime.strptime(check_in_time, '%I %p').time()
        check_in = datetime.combine(check_in_date, check_in_time)
        check_out = check_in + timedelta(hours=duration)
        check_out_date = check_out.date() 
        room = get_object_or_404(Room, id=room_id)
        email = request.user.email
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.user = request.user
            guest.first_name = form.cleaned_data.get('first_name')
            guest.last_name = form.cleaned_data.get('last_name')
            guest.address = form.cleaned_data.get('address')
            guest.phone = form.cleaned_data.get('phone')
            guest.date_of_birth = form.cleaned_data.get('date_of_birth')
            guest.save()
        else:
            check_in_date = check_in_date.date()
            check_out_time = check_out.time()
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
        
        form2 = BookingForm(request.POST)
        if form2.is_valid():
            booking = form2.save(commit=False)
            booking.guest = guest
            booking.check_in = check_in
            booking.check_out = check_out
            room_id = request.POST.get('room_id')
            room = get_object_or_404(Room, id=room_id) 
            booking.room = room
            booking.total_amount = room.room_type.price

            booking.duration = timedelta(hours=duration)
            booking.save()
            return render(request, "content/book_step4.html", {
                "check_in": check_in,
                "check_out": check_out,
                "email": email,
            })
        else:
            print(form2.errors)  
            return render(request, "content/book_step3.html", {
                "form": form,
                "check_in": check_in,
                "room": room,
                "email": email,
            })

    else:
        check_in_unformat = request.GET.get('book_check_in_date')
        check_in_time = request.GET.get("book_check_in_time")
        duration = request.GET.get('book_duration')
        duration = int(duration)
        date_object = datetime.strptime(check_in_unformat, '%b. %d, %Y')
        check_in_date = date_object.strftime('%Y-%m-%d')
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date() if check_in_date else None

        start_time = datetime.strptime(check_in_time, '%H:%M').time() 
        start_datetime = datetime.combine(check_in_date, start_time)
        end_datetime = start_datetime + timedelta(hours=duration)

        check_out_date = end_datetime.date()
        check_out_time = end_datetime.time()
        check_in_time = start_datetime.time()

        room_id = request.GET.get('roomtype')
        room = get_object_or_404(Room, id=room_id)
        email = request.user.email
        price = room.room_type.price
        form = GuestForm()  
        

        host = request.get_host()

        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': price,
            'item_name': "any",
            'invoice': str(uuid.uuid4()),
            'currency_code': 'PHP',
            'notify_url': "https://9b79-2001-4453-6c4-6400-1079-4938-7e0e-ac41.ngrok-free.app/paypal-ipn/",
            'return_url': "http://127.0.0.1:8000/rooms/", 
            'custom': "standard"
        }



        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        context = {
            'form': form,
            'duration': duration,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'check_in_time': check_in_time,
            'check_out_time': check_out_time,
            'room': room,
            'email': email,
            'paypal': paypal_payment,
        }

        return render(request, 'content/book_step3.html', context)


def book_view4(request):
    email = request.user.email
    context = {
        "email":email,
    }
    return render(request, "content/book_step4.html", context)

def calendar_view(request):
    return render(request, "content/calendar.html")


from datetime import datetime, timedelta
from django.db.models import Q

def search_room(request):
    if request.method == 'GET':
        check_in_unformat = request.GET.get('check_in_date')
        # Parse the string into a datetime object
        date_object = datetime.strptime(check_in_unformat, '%b. %d, %Y')
        check_in_date = date_object.strftime('%Y-%m-%d')
        capacity = request.GET.get("capacity")
        checkin_time = request.GET.get("checkin_time", "12:00") 
        duration = request.GET.get("duration", 8)  

        # Convert check_in_date to a date object
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date() if check_in_date else None

        # Convert duration to integer
        duration = int(duration) if isinstance(duration, str) and duration.isdigit() else 8

        # Filter rooms by capacity
        rooms = Room.objects.filter(room_type__capacity__gte=capacity)

        # Exclude rooms that are booked during the requested time range
        if check_in_date and checkin_time:
            start_time = datetime.strptime(checkin_time, '%H:%M').time()  # 24-hour format
            start_datetime = datetime.combine(check_in_date, start_time)
            end_datetime = start_datetime + timedelta(hours=duration)

            
            rooms = rooms.exclude(
                Q(booking__check_in__lt=end_datetime) & Q(booking__check_out__gt=start_datetime)
            )

        check_in_date_str = date_object.strftime('%b. %d, %Y')  

        context = {
            'rooms': rooms,
            'capacity': capacity,
            'check_in_date': check_in_date_str,
            'duration': duration,
            'checkin_time': checkin_time
        }

        return render(request, 'content/booking.html', context)


def payment(request):
    amount = 10000
    description = "Lac resort"
    remarks = "Please check your email for booking details"

    payment_link = create_payment_link(amount, description, remarks)
    checkout_url = payment_link['data']['attributes']['checkout_url']

    return HttpResponseRedirect(checkout_url)

def test_payment(request):
    return render(request, 'content/test_payment.html')