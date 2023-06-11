from django import forms
from .models import Itinerary, Accommodation
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.forms import UserCreationForm

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['title', 'description','destination', 'start_date', 'end_date']

class AccommodationBookingForm(forms.Form):
    accommodation = forms.ModelChoiceField(queryset=Accommodation.objects.all())
    check_in_date = forms.DateField()
    check_out_date = forms.DateField()

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text='Enter your email address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )