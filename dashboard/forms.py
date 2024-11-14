from django import forms
from content.models import Room, RoomType


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
    
