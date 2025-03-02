from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.room_view, name='rooms'),
    path('room/<int:id>/', views.room_detail_view, name='room_detail'),
    path('service/', views.service_view, name='service'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('play/', views.play_view, name='play'),
    path('terms/', views.terms_view, name='terms'),
    path('policy/', views.policy_view, name='policy'),
    path('booking/step1', views.book_view1, name='book_1'),
    path('booking/step2', views.book_view2, name='book_2'),
    path('booking/step3', views.book_view3, name='book_3'),
    path('booking/step4/<int:temp_id>', views.book_view4, name='book_4'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('search/', views.search_room, name='search_room'),
    path('paypal-ipn/', views.paypal_ipn, name='paypal-ipn'),
    path('get_fully_book/', views.getFullyBookDates, name='get_fully_book'),
    path('initial_search/', views.initial_search, name='initial_search'),
    path('dynamic_search/', views.dynamic_search, name='dynamic_search'),
    path('test_data/', views.test_data, name='test_data'),
    path('get_provinces/', views.get_provinces, name='get_provinces'),
    path('get_municipalities/', views.get_municipalities, name='get_municipalities'),
    path('test_upload/', views.test_upload, name='test_upload'),
    path('fetch_available_times/', views.fetch_available_times, name='fetch_available_times'),
    path('fetch_duration/', views.fetch_duration, name='fetch_duration'),
]
