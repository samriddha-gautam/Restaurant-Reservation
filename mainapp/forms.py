from django import forms
from .models import Reservation, VIPCustomer,VIPReservation,Customer
from django.contrib.auth.models import User


class CustomerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    phone = forms.CharField(widget=forms.TextInput())  # New phone number field

    class Meta:
        model = Customer
        fields = ["first_name","last_name","username", "password", "email", "phone"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")
        return uname
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        return phone
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("email is required.")
        return email
    
class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())





class CustomerReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Reservation Date'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Reservation Time'
    )
    num_guests = forms.IntegerField(
        min_value=1,
        max_value=10,
        label="Number of Guests"
    )
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

class SetCredentialsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class VIPCustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class VIPReservationForm(forms.ModelForm):
    date = forms.DateField() 
    time = forms.TimeField()
    num_guests = forms.IntegerField(min_value=1, max_value=50, label="Number of Guests")

    class Meta:
        model = VIPReservation
        fields = ['date', 'time', 'num_guests', 'table', 'special_notes']
        widgets = {
            'vip_customer': forms.HiddenInput(),  # Hide vip_customer
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['vip_customer'].queryset = VIPCustomer.objects.none()