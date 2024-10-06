from django import forms
from .models import Guest
from .models import Booking
from django.core.validators import RegexValidator

class GuestForm(forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  
        message="Please enter a valid phone number."
    )
    
    phone = forms.CharField(validators=[phone_validator])
    
    class Meta:
        model = Guest
        exclude = ['user']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking

        exclude = ['check_out', 'total_amount', 'duration', 'start_time', 'end_time', 'guest', 'room', 'check_in']

