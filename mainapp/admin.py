from django.contrib import admin
from .models import Reservation,Table

from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    # Customize the table display in the admin interface
    list_display = ('table_number', 'capacity')

    actions = ['free_table']

    def free_table(self, modeladmin, request, queryset):
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
    list_display = ('first_name','last_name', 'date', 'time', 'num_guests', 'table')
    list_filter = ('date',)