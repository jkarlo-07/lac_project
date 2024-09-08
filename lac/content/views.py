from django.core.mail import BadHeaderError
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import RoomType
from lac.utils.email_utils import send_email_contact
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    room_id = request.GET.get('roomtype')

    room = get_object_or_404(RoomType, id=room_id)
    email = request.user.email
    
    context = {
        'check_in': check_in,
        'check_out': check_out,
        'room': room,
        'email': email,
    }
    return render(request, 'content/book_step3.html', context)

def book_view4(request):
    return render(request, "content/book_step4.html")

def calendar_view(request):
    return render(request, "content/calendar.html")


