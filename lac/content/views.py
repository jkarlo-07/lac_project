from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "content/index.html")

def room_view(request):
    return render(request, "content/rooms.html")