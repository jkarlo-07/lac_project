from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('users/login', views.login_view, name='login'),
    path('users/signup', views.signup_view, name='signup'),
]
