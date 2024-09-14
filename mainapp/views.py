from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView,CreateView,FormView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
import random  #line 1-5 imported for OTP handling
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date
from urllib import request
from .models import Reservation,Table, VIPCustomer,Customer
from .forms import CustomerReservationForm, CredentialsForm , OTPForm, SetCredentialsForm , VIPReservation,VIPReservationForm,CustomerRegistrationForm,CustomerLoginForm,VIPCustomerLoginForm


def index(request):
    return render(request, 'users/homepage.html')
def about_us(request):
    return render(request, 'users/about_us.html')
def gallery(request):
    return render(request, 'users/gallery.html')
def find_us(request):
    return render(request, 'users/find_us.html')
# def vip_index(request):
#     return render(request, 'users/VIP.html')


def registration_success(request):
    customers = Customer.objects.all()
    return render(request, 'users/registration_success.html', {'customers': customers})


class CustomerRegistrationView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("mainapp:registration_success")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        phone = form.cleaned_data.get("phone")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'Username already exists')
            return self.form_invalid(form)

        # Check if a user with the same email address already exists
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Email address already in use')
            return self.form_invalid(form)

        # Create the user and the Customer instance
        new_user = User.objects.create_user(username, email, password)
        form.instance.user = new_user
        form.instance.first_name = first_name
        form.instance.last_name = last_name
        form.instance.phone = phone
        form.save()
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

            # Store custom session data
            self.request.session['user_id'] = usr.id  # Changed to user_id for consistency
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
        user_id = request.session.get('user_id')  # Consistent with what is stored in the session
        email = request.session.get('email')

        # Optional: Fetch customer data based on the session data
        try:
            customer = Customer.objects.get(user__id=user_id)
        except Customer.DoesNotExist:
            customer = None

        # Pass the session data and customer info to the template
        return render(request, self.template_name, {
            'user_id': user_id,
            'email': email,
            'customer': customer,  # Include customer info
        })


def add_reservation(request):
    if request.method == 'POST':
        form = CustomerReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            
            # Get the customer linked to the current user
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    customer = Customer.objects.get(user_id=user_id)
                    reservation.customer = customer
                    reservation.save()
                    messages.success(request, "Reservation successfully added!")
                    return redirect('mainapp:reservation_success')
                except Customer.DoesNotExist:
                    messages.error(request, "Customer not found. Please log in.")
            else:
                messages.error(request, "User ID not found in session.")
                return redirect('mainapp:customer_login')

    else:
        form = CustomerReservationForm()

    return render(request, 'users/add_reservation.html', {'form': form})

def reservation_success(request):
    return render(request, 'users/reservation_success.html')


# VIP Section starts here

otp_storage = {}
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))  # 6-digit OTP
def send_otp(email, otp):
    subject = 'VIP OTP'
    message = f'Your VIP OTP code is {otp}. Feel Grateful we are letting you enter our VIP section. Peasant!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
def credentials_view(request):
    if request.method == 'POST':
        form = CredentialsForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if VIPCustomer.objects.filter(email=email).exists():
                messages.error(request, 'Already a VIP customer. Please log in.')
                return redirect('mainapp:vip_customer_login')
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
            email = request.session.get('email')
            
            if not email:
                messages.error(request, 'Session expired. Please request a new OTP.')
                return redirect('mainapp:vip_credentials')  # Ensure this is correct

            stored_otp = otp_storage.get(email)
            if stored_otp == otp:
                del otp_storage[email]

                # Get VIP data from session
                vip_data = request.session.pop('vip_data', None)
                customer_instance = None  # Initialize to None

                if vip_data:
                    # Check if the email exists in the Customer model but not in the VIPCustomer model
                    if not VIPCustomer.objects.filter(email=email).exists():
                        customer = Customer.objects.filter(email=email).first()

                        if customer:
                            # If the customer exists in the Customer model, delete it and transfer data to VIPCustomer
                            customer_instance = Customer.objects.get(email=email)
                            customer_instance.delete()

                            # Create new VIP customer using the VIP data
                            VIPCustomer.objects.create(
                                first_name=vip_data['first_name'],
                                last_name=vip_data['last_name'],
                                phone=vip_data['phone'],
                                email=email,
                                user=customer_instance.user
                            )
                        else:
                            VIPCustomer.objects.create(
                                first_name=vip_data['first_name'],
                                last_name=vip_data['last_name'],
                                phone=vip_data['phone'],
                                email=email,
                                user=None  # Attach user if exists
                            )    

                # After successful customer migration, redirect to set credentials page
                return redirect('mainapp:set_credentials',email=email)

            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()
    
    return render(request, 'VIP/verify_otp.html', {'form': form})

def set_credentials_view(request,email):
    # email = request.session.get('email')
    
    # if not email:
    #     messages.error(request, 'Session expired. Please complete the process again.')
    #     return redirect('mainapp:vip_credentials')  # Ensure this is correct

    try:
        vip_customer = VIPCustomer.objects.get(email=email)
    except VIPCustomer.DoesNotExist:
        messages.error(request, 'VIP Customer not found. Please complete the registration process.')
        return redirect('mainapp:vip_credentials')  # Ensure this is correct

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save(commit=False)  # Don't save to the database yet
            user.email = email  # Set email
            user.username = form.cleaned_data['username']  # Get username from form
            user.save()

            # Associate the VIPCustomer with this newly created user
            vip_customer.user = user
            vip_customer.save()

            # if customer_instance:
            #     customer_instance.delete()

            # Log in the user and redirect to VIP profile or home page
            login(request, user)
            messages.success(request, "Credentials successfully set. Welcome to the VIP section!")
            return redirect('mainapp:vip_userprofile_')  # Ensure this is correct
    else:
        form = UserCreationForm()  # Present an empty form if not POST

    return render(request, 'VIP/set_credentials.html', {'form': form})


def add_vip_reservation(request):
    if request.method == 'POST':
        form = VIPReservationForm(request.POST)
        if form.is_valid():
            # Save the reservation if valid
            form.save()
            messages.success(request, "VIP Reservation Successfully added")
            return redirect('mainapp:vip_reservation_success')
    else:
        form = VIPReservationForm()
    return render(request, 'VIP/vip_reservation.html', {'form': form})


def vip_reservation_success(request):
    return render(request, 'VIP/vip_reservation_success.html')



class VIPCustomerLoginView(FormView):
    template_name = "VIP/vip_login.html"
    form_class = VIPCustomerLoginForm
    success_url = reverse_lazy("mainapp:vip_userprofile_")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        vipuser = authenticate(username=uname, password=pword)
        
        if vipuser is not None and VIPCustomer.objects.filter(user=vipuser).exists():
            login(self.request, vipuser)

            # Store custom session data
            self.request.session['user_id'] = vipuser.id  # Changed to user_id for consistency
            self.request.session['email'] = vipuser.email
            
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid credentials or you are not a VIP customer.")
            return self.form_invalid(form)

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        return next_url if next_url else self.success_url

class VIPUserProfileView(LoginRequiredMixin, View):
    template_name = "VIP/vip_user_profile.html"

    def get(self, request):
        # Fetch the currently logged-in user
        user = request.user

        # Try to fetch the VIPCustomer linked to this user
        try:
            VIPcustomer = VIPCustomer.objects.get(user=user)
        except VIPCustomer.DoesNotExist:
            VIPcustomer = None

        # Pass the VIP customer info and user data to the template
        return render(request, self.template_name, {
            'VIPcustomer': VIPcustomer,
            'user': user  # Pass the user to the template
        })



def VIPCustomerLogoutView(request):
    logout(request)
    return redirect(request,'VIP/VIP.html')
