from django.contrib import admin
from .models import Reservation,Table

from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    # Customize the table display in the admin interface
    list_display = ('table_number', 'capacity','is_occupied')

    actions = ['free_table']

    def free_table(self,request, queryset):
        for table in queryset:
            if table.reservation:
                table.reservation.delete()
            table.reservation = None
            table.save()
        self.message_user(request, f"{queryset.count()} tables freed")
    free_table.short_description = 'Free Table'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # Customize the reservation display in the admin interface
    list_display = ('first_name','last_name', 'date', 'time', 'num_guests', 'table','status','notes')
    list_filter = ('date','time',)

    actions = ['mark_as_confirmed','mark_as_canceled','mark_as_pending']

    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')
        self.message_user(request, "Selected reservations have been marked as pending.")
    mark_as_pending.short_description = 'Mark Pending'


    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, "Selected reservations have been marked as confirmed.")
    mark_as_confirmed.short_description = 'Mark Confirmed'

    def mark_as_canceled(self, request, queryset):
        queryset.update(status='canceled')
        self.message_user(request, "Selected reservations have been marked as canceled.")
    mark_as_canceled.short_description = 'Mark canceled'
    