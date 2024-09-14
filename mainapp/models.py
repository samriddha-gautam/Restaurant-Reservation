from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True ,null=True, blank=False)  # Added uniqueness to prevent duplicates
    email = models.EmailField(unique=True ,blank=False)  # Ensure uniqueness across customers

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
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
    num_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Reservation for {self.first_name} {self.last_name} on {self.date} at {self.time} (Table {self.table.table_number})"

    def save(self, *args, **kwargs):
        existing_customer = Customer.objects.filter(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone
        ).first()
        if existing_customer:
            self.customer = existing_customer
        else:
            self.customer = Customer.objects.create(
                first_name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                phone=self.phone
            )
        super().save(*args, **kwargs)

class VipTable(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"VIP Table #{self.table_number} ({self.capacity} seats)"

class VIPCustomer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    vip_since = models.DateField(default=date.today)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (VIP since {self.vip_since})"

    def save(self, *args, **kwargs):
        existing_vip_customer = VIPCustomer.objects.filter(
            email=self.email,
            phone=self.phone
        ).first()

        if existing_vip_customer:
            self.pk = existing_vip_customer.pk  # Prevent duplicate VIP entries
        super().save(*args, **kwargs)

class VIPReservation(models.Model):
    vip_customer = models.ForeignKey(VIPCustomer, on_delete=models.CASCADE, related_name='vip_reservations')
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    table = models.ForeignKey(VipTable, on_delete=models.CASCADE, related_name='vip_reservations')
    special_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"VIP Reservation for {self.vip_customer} on {self.date} at {self.time}"
