from django.shortcuts import render

def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

def guest_view(request):
    return render(request, "dashboard/guest.html")

def room_view(request):
    return render(request, "dashboard/room.html")

def booking_view(request):
    return render(request, "dashboard/booking.html")
