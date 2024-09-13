from django import forms
from .models import Reservation,VIPReservation,Customer
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'    
 
class CustomerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    phone_number = forms.CharField(widget=forms.TextInput())  # New phone number field

    class Meta:
        model = Customer
        fields = ["first_name","last_name","username", "password", "email", "phone_number"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")
        return uname
    
class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



# First form
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'phone', 'date', 'time', 'num_guests', 'table']

# Second form with custom widgets for date and time
class CustomReservationForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput) 
    time = forms.TimeField(widget=TimeInput)
    num_guests = forms.IntegerField(min_value=1, max_value=10, label="Number of Guests")

    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'phone', 'date', 'time', 'num_guests', 'table']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

class CredentialsForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='First Name')
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Last Name')
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Phone Number')


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)  


class VIPReservationForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput) 
    time = forms.TimeField(widget=TimeInput)
    num_guests = forms.IntegerField(min_value=1, max_value=50, label="Number of Guests")

    class Meta:
        model = VIPReservation
        fields = ['vip_customer', 'date', 'time', 'num_guests', 'table', 'special_notes']