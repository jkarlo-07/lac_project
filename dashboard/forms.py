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
