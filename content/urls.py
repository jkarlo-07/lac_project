from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.room_view, name='rooms'),
    path('service/', views.service_view, name='service'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('booking/step1', views.book_view1, name='book_1'),
    path('booking/step2', views.book_view2, name='book_2'),
    path('booking/step3', views.book_view3, name='book_3'),
    path('booking/step4', views.book_view4, name='book_4'),
    path('calendar', views.calendar_view, name='calendar'),
    path('search', views.search_room, name='search_room'),
    path('payment/', views.payment, name='payment'),
    path('test_payment/', views.test_payment, name='test_payment'),
]
