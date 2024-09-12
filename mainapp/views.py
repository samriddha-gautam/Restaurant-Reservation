from datetime import date
from urllib import request
from django.shortcuts import redirect, render
from .models import Reservation,Table
from .forms import CustomReservationForm, ReservationForm


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