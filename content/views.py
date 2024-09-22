from django.core.mail import BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import RoomType
from lac.utils.email_utils import send_email_contact
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import GuestForm, BookingForm
from datetime import timedelta, time
from .models import Room

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
        
        room = get_object_or_404(RoomType, id=room_id)
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
            print(form.errors)  
            return render(request, "content/book_step3.html", {
                "form": form,
                "check_in": check_in,
                "room": room,
                "email": email,
            })
        
        form2 = BookingForm(request.POST)
        if form2.is_valid():
            booking = form2.save(commit=False)
            booking.user = request.user
            booking.check_in_date = request.POST.get('check_in_date')
            booking.check_out_date = "2002-01-01"
            booking.total_amount = "1000"
            room = get_object_or_404(Room, id=1)  # Get the room with ID 1
            booking.room = room
            booking.duration = timedelta(hours=12)
            booking.start_time = time(8, 0)
            booking.end_time = time(20,0)
            booking.save()
            return redirect("users:login")
        else:
            print(form2.errors)  
            return render(request, "content/book_step3.html", {
                "form": form,
                "check_in": check_in,
                "room": room,
                "email": email,
            })


    else:
        check_in = request.GET.get('check_in')
        room_id = request.GET.get('roomtype')
        room = get_object_or_404(RoomType, id=room_id)
        email = request.user.email
        
        form = GuestForm()  
        context = {
            'form': form,
            'check_in': check_in,
            'room': room,
            'email': email,
        }
        return render(request, 'content/book_step3.html', context)

def book_view4(request):
    return render(request, "content/book_step4.html")

def calendar_view(request):
    return render(request, "content/calendar.html")



