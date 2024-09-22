from django import forms
from .models import Guest
from .models import Booking

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        # Exclude the user field, since we will handle it in the view
        exclude = ['user']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking

        exclude = ['check_out_date', 'total_amount', 'duration', 'start_time', 'end_time', 'user', 'room']

