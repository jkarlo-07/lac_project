from django import forms
from content.models import Room, RoomType
from django.core.validators import RegexValidator

class ExistingRoomForm(forms.ModelForm):
    class Meta:
        model = Room

        fields = ['room_number']
        exclude = ['room_type']

class NewRoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType

        fields = ['room_type', 'description', 'price', 'capacity', 'picture']

class UpdateRoomTypeForm(forms.Form):
    room_type = forms.CharField(max_length=50)
    description = forms.CharField(max_length=250)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    capacity = forms.IntegerField()
    picture = forms.ImageField(required=False)
    is_cottage_required = forms.CharField(max_length=10, required=False)

class UpdateGuestForm(forms.Form):
    first_name = forms.CharField(max_length=75)
    last_name = forms.CharField(max_length=75)
    address = forms.CharField(max_length=200)
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  
        message="Please enter a valid phone number."
    )
    phone = forms.CharField(max_length=30, validators=[phone_validator])
    date_of_birth = forms.DateField(
        input_formats=['%Y-%m-%d'],  
        widget=forms.DateInput(
            attrs={'placeholder': 'YYYY-MM-DD'}
        ),
        error_messages={'invalid': 'Enter date in YYYY-MM-DD format.'}
    )

class UpdateBookingForm(forms.Form):
    adult_count = forms.IntegerField()
    kid_count = forms.IntegerField()
    room = forms.CharField(max_length=25)