from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('guest', views.guest_view, name='guest'),
    path('booking', views.booking_view, name='booking'),
    path('room', views.room_view, name='room'),
    path('book_form', views.book_form_view, name='book_form'),
    path('roomt_form', views.room_type_view, name='roomt_form'),
    path('addroom_form', views.add_room_view, name='addroom_form'),
    path('sample-sales-data/', views.sample_sales_data, name='sample_sales_data'),
    path('option_room', views.option_room_view, name='option_room'),
    path('add_existing_room', views.add_existing_room, name='add_existing_room'),
    path('add_new_room_type', views.add_new_room_type, name='add_new_room_type'),
    path('fetch_all_rooms', views.fetch_all_rooms, name='fetch_all_rooms'),
    path('delete_room', views.delete_room, name='delete_room'),
    path('delete_roomtype', views.delete_roomtype, name='delete_roomtype'),
    path('update_room', views.update_room, name='update_room'),
    path('update_room_type', views.update_room_type, name='update_room_type'),
]
