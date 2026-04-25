from django.contrib import admin

# Register your models here.
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
    'customer_name',
    'customer_phone',
    'customer',
    'employee',
    'service',
    'appointment_date',
    'appointment_time',
    'status'
)
    list_filter = ('status', 'appointment_date', 'employee')
    search_fields = ('customer__username', 'service__name')
