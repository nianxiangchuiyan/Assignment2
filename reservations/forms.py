from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Reservation


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


from django import forms


class TimeOnlyReservationForm(forms.Form):
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
