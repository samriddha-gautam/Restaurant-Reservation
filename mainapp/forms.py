from django import forms
from .models import Reservation

# First form
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'phone', 'date', 'time', 'num_guests', 'table']

# Second form with custom widgets for date and time
class CustomReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Reservation Date"
    ) 
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}),label="Reservation Time")
    num_guests = forms.IntegerField(min_value=1, max_value=10, label="Number of Guests")

    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'phone', 'date', 'time', 'num_guests', 'table']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }