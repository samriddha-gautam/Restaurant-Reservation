import random  #line 1-5 imported for OTP handling
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date
from urllib import request
from django.shortcuts import redirect, render
from .models import Reservation,Table
from .forms import CustomReservationForm, ReservationForm , CredentialsForm , OTPForm


def index(request):
  return render(request, 'users/homepage.html')

def dashboard(request):
##Display dashboard for staffs
  reservations = Reservation.objects.filter(date__gte=date.today())  # Filter for future reservations
  return render(request, 'staffs/dashboard.html', {'reservations': reservations})

def add_reservation(request):
    if request.method == 'POST':
        form = CustomReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the reservation if valid
            return redirect('reservation_success')  # Redirect on successful reservation
    else:
        form = ReservationForm()  # Show empty form on GET requests

    # Ensure the form is rendered in all cases, including when the POST data is invalid
    return render(request, 'users/add_reservation.html', {'form': form})

def reservation_success(request):
    return render(request, 'users/reservation_success.html')


otp_storage = {}

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))  # 6-digit OTP

def send_otp(email, otp):
    subject = 'VIP OTP'
    message = f'Your VIP OTP code is {otp}. Feel Grateful we are letting you enter our VIP section. Peasant!!!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

def credentials_view(request):
    if request.method == 'POST':
        form = CredentialsForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = generate_otp()
            otp_storage[email] = otp  # Store OTP temporarily
            send_otp(email, otp)
            request.session['email'] = email  # Store email in session
            return redirect('verify_otp')  # Redirect to OTP verification page
    else:
        form = CredentialsForm()
    return render(request, 'VIP/credentials.html', {'form': form})

def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            email = request.session.get('email')  # Retrieve email from session
            if not email:
                messages.error(request, 'Session expired. Please request a new OTP.')
                return redirect('credentials_view')  # Redirect to request new OTP
            stored_otp = otp_storage.get(email)
            if stored_otp == otp:
                del otp_storage[email]  # Remove OTP after verification
                return render(request, 'VIP/VIP.html')  # Redirect to VIP page
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()
    return render(request, 'VIP/verify_otp.html', {'form': form})
