from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('guest', views.guest_view, name='guest'),
    path('booking', views.booking_view, name='booking'),
    path('room', views.room_view, name='room'),
    path('book_form', views.book_form_view, name='book_form'),
]
