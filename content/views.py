from django.core.mail import BadHeaderError
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
        name =  "hello"
        email = "achicokarlo@gmail.com"
        subject = "ewam"
        message = "hoy"
        if name and email and subject and message:
            try:
                result = send_email_contact(name, email, subject, message, 'jkma.achico@gmail.com', 'content/email_template.html')
                
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
        'notify_url': "https://www.lacresort.com/paypal-ipn/",
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
            room = get_object_or_404(Room, id=room_id)

            request.session['room'] = str(room.id) 
            request.session['total_amount'] = str(room.room_type.price) 
            request.session['duration'] = str(duration) 
            return redirect('content:book_2')

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
    email = request.user.email
    context = {
        "email":email,
        "details":details,
    }
    return render(request, "content/book_step4.html", context)

@login_required(login_url="users:login")
def calendar_view(request):
    return render(request, "content/calendar.html")


from datetime import datetime, timedelta
from django.db.models import Q

def search_room(request):
    if request.method == 'GET':
        check_in_unformat = request.GET.get('check_in_date')
        date_object = datetime.strptime(check_in_unformat, '%b. %d, %Y')
        check_in_date = date_object.strftime('%Y-%m-%d')
        capacity = request.GET.get("capacity")
        checkin_time = request.GET.get("checkin_time", "12:00") 
        duration = request.GET.get("duration", 8)  

        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date() if check_in_date else None

        duration = int(duration) if isinstance(duration, str) and duration.isdigit() else 8

        rooms = Room.objects.filter(room_type__capacity__gte=capacity)

        if check_in_date and checkin_time:
            start_time = datetime.strptime(checkin_time, '%H:%M').time()  
            start_datetime = datetime.combine(check_in_date, start_time)
            end_datetime = start_datetime + timedelta(hours=duration)

            
            rooms = rooms.exclude(
                Q(booking__check_in__lt=end_datetime) & Q(booking__check_out__gt=start_datetime)
            )

        rooms = rooms.distinct('room_type')

        check_in_date_str = date_object.strftime('%b. %d, %Y')  

        context = {
            'rooms': rooms,
            'capacity': capacity,
            'check_in_date': check_in_date_str,
            'duration': duration,
            'checkin_time': checkin_time
        }

        return render(request, 'content/booking.html', context)
