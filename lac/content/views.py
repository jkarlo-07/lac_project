from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import RoomType

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
                html_message = render_to_string('content/email_template.html', {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message
                })
                
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject,
                    plain_message,  
                    email,  
                    ['lacresortfarm@gmail.com'], 
                    html_message=html_message,  
                    fail_silently=False,
                )
                
                return JsonResponse({'message': 'Message has been sent!'})
            
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=400)
            
            except Exception as e:
                return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
        
        else:
            return JsonResponse({'error': 'Make sure all fields are entered and valid.'}, status=400)
    
    return render(request, 'content/contact.html')

def about_view(request):
    return render(request, "content/about.html")

def book_view1(request):
    return render(request, "content/booking.html")

def book_view2(request):
    return render(request, "content/book_step2.html")

def book_view3(request):
    return render(request, "content/book_step3.html")

def book_view4(request):
    return render(request, "content/book_step4.html")
