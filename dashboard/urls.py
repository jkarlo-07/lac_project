from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('guest', views.guest_view, name='guest'),
    path('booking', views.booking_view, name='booking'),
    path('room', views.room_view, name='room'),
    path('manage_email', views.manage_email_view, name='manage_email'),
    path('amenities', views.amenities_view, name='amenities'),
    path('book_form', views.book_form_view, name='book_form'),
    path('roomt_form', views.room_type_view, name='roomt_form'),
    path('addroom_form', views.add_room_view, name='addroom_form'),
    path('get_data', views.get_data, name='get_data'),
    path('option_room', views.option_room_view, name='option_room'),
    path('add_existing_room', views.add_existing_room, name='add_existing_room'),
    path('add_new_room_type', views.add_new_room_type, name='add_new_room_type'),
    path('fetch_all_rooms', views.fetch_all_rooms, name='fetch_all_rooms'),
    path('delete_room', views.delete_room, name='delete_room'),
    path('delete_roomtype', views.delete_roomtype, name='delete_roomtype'),
    path('update_room', views.update_room, name='update_room'),
    path('update_room_type', views.update_room_type, name='update_room_type'),
    path('delete_guest', views.delete_guest, name='delete_guest'),
    path('update_guest', views.update_guest, name='update_guest'),
    path('delete_booking', views.delete_booking, name='delete_booking'),
    path('get_time', views.get_time, name='get_time'),
    path('get_rooms', views.get_rooms, name='get_rooms'),
    path('update_booking', views.update_booking, name='update_booking'),
    path('add_booking', views.add_booking, name='add_booking'),
    path('change_booking_status', views.change_booking_status, name='change_booking_status'),
    path('add_amenities', views.add_amenities, name='add_amenities'),
]
