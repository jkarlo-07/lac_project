from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('users/login', views.login_view, name='login'),
    path('users/signup', views.signup_view, name='signup'),
    path('users/signupsuc', views.signupsuc_view, name='signupsuc'),
    path('users/forgot', views.forgot_view, name='forgot'),
    path('users/logout', views.logout_view, name='logout'),
]
