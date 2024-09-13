from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView,CreateView,FormView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
import random  #line 1-5 imported for OTP handling
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date
from urllib import request
from .models import Reservation,Table, VIPCustomer,Customer
from .forms import CustomReservationForm, ReservationForm , CredentialsForm , OTPForm , VIPReservation,VIPReservationForm,CustomerRegistrationForm,CustomerLoginForm


def index(request):
  return render(request, 'users/homepage.html')

# def dashboard(request):
# ##Display dashboard for staffs
#   reservations = Reservation.objects.filter(date__gte=date.today())  # Filter for future reservations
#   return render(request, 'staffs/dashboard.html', {'reservations': reservations})

def registration_success(request):
    customers = Customer.objects.all()
    return render(request, 'users/registration_success.html', {'customers': customers})


class CustomerRegistrationView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("mainapp:registration_success")
    # after successful register redirect to customer_list(name)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'Username already exists')
            return self.form_invalid(form)

        # Check if a user with the same email address already exists
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Email address already in use')
            return self.form_invalid(form)

        new_user = User.objects.create_user(username, email, password)
        form.instance.user = new_user
        login(self.request, new_user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


def CustomerLogoutView(request):
    logout(request)
    return redirect('mainapp:index')

class CustomerLoginView(FormView):
    template_name = "registration/login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("mainapp:userprofile_")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
            
            # Store custom session data (e.g., user_id, username)
            self.request.session['customer_id'] = usr.id
            self.request.session['email'] = usr.email
        else:
            return render(self.request, self.template_name, {"form": self.form_class(), "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class UserProfileView(LoginRequiredMixin, View):
    template_name = "users/user_profile.html"

    def get(self, request):
        # Retrieve session data
        user_id = request.session.get('user_id')
        username = request.session.get('username')

        # Optional: Fetch customer data based on the session data
        try:
            customer = Customer.objects.get(user__id=user_id)
        except Customer.DoesNotExist:
            customer = None

        # Pass the session data and customer info to the template
        return render(request, self.template_name, {
            'user_id': user_id,
            'username': username,
            # 'customer': customer,
        })

def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Save the reservation (this will handle customer creation/linking)
            form.save()
            messages.success(request, "Reservation successfully created.")
            return redirect('reservation_success')  # Redirect to a success page
    else:
        form = ReservationForm()  # Show an empty form on GET requests

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
            otp_storage[email] = otp
            print(otp_storage)  # Store OTP temporarily
            send_otp(email, otp)
            request.session['email'] = email  # Store email in session
            # Store VIP customer data in session
            vip_data = {
                'first_name': form.cleaned_data.get('first_name', ''),
                'last_name': form.cleaned_data.get('last_name', ''),
                'phone': form.cleaned_data.get('phone', ''),
                'email': email,
                'address': form.cleaned_data.get('address', ''),
            }
            request.session['vip_data'] = vip_data

            return redirect('mainapp:verify_otp')  # Redirect to OTP verification page
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
                return redirect('mainapp:redentials_view')  # Redirect to request new OTP
    
            stored_otp = otp_storage.get(email)
            if stored_otp == otp:
                del otp_storage[email]  # Remove OTP after verification
                
                # Retrieve VIP data from session
                vip_data = request.session.pop('vip_data', None)
                if vip_data:
                    if not VIPCustomer.objects.filter(email=email).exists():
                        # Create new VIP customer
                        VIPCustomer.objects.create(
                            first_name=vip_data['first_name'],
                            last_name=vip_data['last_name'],
                            phone=vip_data['phone'],
                            email=email,
                        )
                
                return render(request, 'VIP/VIP.html')  # Redirect to VIP page
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()
    return render(request, 'VIP/verify_otp.html', {'form': form})


def vip_reservation_view(request):
    if request.method == 'POST':
        form = VIPReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the reservation if valid
            return redirect('mainapp:reservation_success')  # Redirect on successful reservation
    else:
        form = VIPReservationForm()

    return render(request, 'VIP/vip_reservation.html', {'form': form})