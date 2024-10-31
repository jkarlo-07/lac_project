from django import forms
from content.models import Room


class ExistingRoomForm(forms.ModelForm):
    class Meta:
        model = Room

        fields = ['room_number', 'room_type']

