from django import forms
from .models import Guest
from .models import Booking
from django.core.validators import RegexValidator
from django import forms
from datetime import date

class BookGuestForm(forms.Form):
    first_name = forms.CharField(max_length=75)
    last_name = forms.CharField(max_length=75)
    address = forms.CharField(max_length=200)
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  
        message="Please enter a valid phone number."
    )
    phone = forms.CharField(max_length=30, validators=[phone_validator])
    
    date_of_birth = forms.DateField(initial=date(2002, 1, 1), widget=forms.SelectDateWidget(years=range(1900, 2025)))
    
    adult_count = forms.IntegerField(initial=1)  # Default value set to 1
    kid_count = forms.IntegerField(initial=0)  # Default value set to 0



class GuestForm(forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  
        message="Please enter a valid phone number."
    )
    
    phone = forms.CharField(validators=[phone_validator])
    
    class Meta:
        model = Guest
        exclude = ['user']

from django import forms
from django.core.validators import RegexValidator
from datetime import date


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking

        exclude = ['check_out', 'total_amount', 'duration', 'start_time', 'end_time', 'guest', 'room', 'check_in']

