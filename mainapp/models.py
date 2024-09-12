from django.db import models
from django.core.validators import MinValueValidator

class Table(models.Model):
    
    table_number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Minimum 1 seat
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table #{self.table_number} ({self.capacity} seats)"

class Reservation(models.Model):
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
        return f"{self.first_name} {self.last_name}- {self.date} at {self.time} (Table {self.table.table_number})"