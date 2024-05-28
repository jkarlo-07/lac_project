from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.room_view, name='rooms'),
    path('service/', views.service_view, name='service'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
]
