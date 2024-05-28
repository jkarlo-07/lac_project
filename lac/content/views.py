from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "content/index.html")

def room_view(request):
    return render(request, "content/rooms.html")

def service_view(request):
    return render(request, "content/service.html")

def contact_view(request):
    return render(request, "content/contact.html")

def about_view(request):
    return render(request, "content/about.html")
