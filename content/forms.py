from django import forms
from .models import Guest

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        # Exclude the user field, since we will handle it in the view
        exclude = ['user']
