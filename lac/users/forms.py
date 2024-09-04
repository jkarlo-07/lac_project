from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from django.core.validators import EmailValidator

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(required=True, validators=[EmailValidator(message="Please enter a valid email address")])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
    