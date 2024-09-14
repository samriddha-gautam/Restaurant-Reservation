from django.contrib import admin
from .models import Reservation,Table,VIPCustomer,VIPReservation,VipTable ,Table, Reservation , Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'email')


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
    

@admin.register(VipTable)
class VipTableAdmin(admin.ModelAdmin):
    # Customize the vip table display in the admin interface
    list_display = ('table_number', 'capacity','is_occupied')

    actions = ['free_table']

    def free_table(self,request, queryset):
        for table in queryset:
            if table.vipreservation:
                table.vipreservation.delete()
            table.vipreservation = None
            table.save()
        self.message_user(request, f"{queryset.count()} VIP tables freed")
    free_table.short_description = 'Free VIP Table'

@admin.register(VIPReservation)
class VIPReservationAdmin(admin.ModelAdmin):
    # Customize the reservation display in the admin interface
    list_display = ('vip_customer', 'date', 'time', 'num_guests', 'table', 'special_notes')
    list_filter = ('date', 'time')

    actions = ['mark_pending', 'mark_confirmed', 'mark_canceled']

    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
        self.message_user(request, "Selected VIP reservations have been marked as pending.")
    mark_pending.short_description = 'Mark VIP Reservation as Pending'

    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, "Selected VIP reservations have been marked as confirmed.")
    mark_confirmed.short_description = 'Mark VIP Reservation as Confirmed'

    def mark_canceled(self, request, queryset):
        queryset.update(status='canceled')
        self.message_user(request, "Selected VIP reservations have been marked as canceled.")
    mark_canceled.short_description = 'Mark VIP Reservation as Canceled'


@admin.register(VIPCustomer)
class VIPCustomerAdmin(admin.ModelAdmin):
    # Customize the VIP customer display in the admin interface
    list_display = ('first_name', 'last_name', 'email', 'phone', 'vip_since')

    search_fields = ('first_name', 'last_name', 'email')  # To search VIP customers by name or email