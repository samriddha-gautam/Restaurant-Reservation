from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the built-in User model
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Table(models.Model):
    
    table_number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Minimum 1 seat
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table #{self.table_number} ({self.capacity} seats)"

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Minimum 1 guest
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Reservation for {self.customer} on {self.date} at {self.time} (Table {self.table.table_number})"

    def save(self, *args, **kwargs):
       # Check if a customer with the given details already exists
       existing_customer = Customer.objects.filter(
           first_name=self.first_name,
           last_name=self.last_name,
           email=self.email,
           phone_number=self.phone
       ).first()
       if existing_customer:
           # If a customer exists, link the reservation to this customer
           self.customer = existing_customer
       else:
           # If no existing customer is found, create a new one
           self.customer = Customer.objects.create(
               first_name=self.first_name,
               last_name=self.last_name,
               email=self.email,
               phone_number=self.phone
           )
       # Ensure the `save` method of the parent class is called
       super().save(*args, **kwargs)


class VipTable(models.Model):
    
    table_number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Minimum 1 seat
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table #{self.table_number} ({self.capacity} seats)"

class VIPCustomer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    vip_since = models.DateField(default=date.today)
    special_requests = models.TextField(blank=True, null=True)  # Optional field for VIP notes

    def __str__(self):
        return f"{self.first_name} {self.last_name} (VIP since {self.vip_since})"

class VIPReservation(models.Model):
    vip_customer = models.ForeignKey(VIPCustomer, on_delete=models.CASCADE)  # Each reservation is linked to a VIP customer
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Minimum 1 guest
    table = models.ForeignKey('VipTable', on_delete=models.CASCADE)  # Reference to the table model
    special_notes = models.TextField(blank=True, null=True)  # Special notes for the reservation

    def __str__(self):
        return f"Reservation for {self.vip_customer} on {self.date} at {self.time}"