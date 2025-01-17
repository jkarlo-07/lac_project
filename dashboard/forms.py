from django import forms
from content.models import Room, RoomType, Amenities
from django.core.validators import RegexValidator

class ExistingRoomForm(forms.ModelForm):
    class Meta:
        model = Room

        fields = ['room_number']
        exclude = ['room_type']

class NewRoomTypeForm(forms.Form):
    class Meta:
        model = RoomType

        fields = ['room_type', 'description', 'price', 'capacity', 'picture']

class AddRoomTypeForm(forms.Form):
    room_type = forms.CharField(max_length=50)
    room_number = forms.CharField(max_length=25)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=250)
    capacity = forms.IntegerField()
    picture = forms.ImageField(required=False)
    picture2 = forms.ImageField(required=False)
    picture3 = forms.ImageField(required=False)
    picture4 = forms.ImageField(required=False)
    picture5 = forms.ImageField(required=False)

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

class AddBookingForm(forms.Form):
    first_name = forms.CharField(max_length=75)
    last_name = forms.CharField(max_length=75)
    address = forms.CharField(max_length=200)
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  
        message="Please enter a valid phone number."
    )
    phone = forms.CharField(max_length=30, validators=[phone_validator])
    dob = forms.DateField(
        input_formats=['%Y-%m-%d'],  
        widget=forms.DateInput(
            attrs={'placeholder': 'YYYY-MM-DD'}
        ),
        error_messages={'invalid': 'Enter date in YYYY-MM-DD format.'}
    )
    checkin_date = forms.CharField(max_length=12)
    checkin_time = forms.CharField(max_length=12)
    duration = forms.CharField(max_length=5)
    room = forms.CharField(max_length=25)
    adult_count = forms.IntegerField()
    kid_count = forms.IntegerField()


class ManageEmailForm(forms.Form):
    main_message = forms.CharField(required=True)
    closing_message = forms.CharField(required=True)
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  
        message="Please enter a valid phone number."
    )
    contact_num = forms.CharField(max_length=30, validators=[phone_validator])
    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': "Please enter a valid email address."
        }
    )

class AddAmenitiesForm(forms.Form):
    name_add = forms.CharField(max_length=25)
    icon_add = forms.ImageField(required=True)

    def clean_name_add(self):
        name_add = self.cleaned_data.get('name_add')
        
        if Amenities.objects.filter(name=name_add).exists():
            raise forms.ValidationError("This name already exists. Please choose a different name.")
        
        return name_add
    
class EditAmenitiesForm(forms.Form):
    name_edit = forms.CharField(max_length=25)
    icon_add = forms.ImageField(required=False)
