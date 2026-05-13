from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'customer_phone',
        'service',
        'employee',
        'appointment_date',
        'appointment_time',
        'get_status_badge'
    )
    list_filter = ('status', 'appointment_date', 'employee', 'service')
    search_fields = ('customer_name', 'customer_phone', 'customer__username', 'service__name')
    readonly_fields = ('created_at', 'get_duration_display')
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer', 'customer_name', 'customer_phone')
        }),
        ('Appointment Details', {
            'fields': ('service', 'employee', 'appointment_date', 'appointment_time')
        }),
        ('Duration', {
            'fields': ('get_duration_display',),
        }),
        ('Notes', {
            'fields': ('note',),
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_status_badge(self, obj):
        status_colors = {
            'pending': '🟡 Pending',
            'confirmed': '✅ Confirmed',
            'completed': '✔️ Completed',
            'cancelled': '❌ Cancelled'
        }
        return status_colors.get(obj.status, obj.status)
    get_status_badge.short_description = 'Status'

    def get_duration_display(self, obj):
        if obj.service:
            return f'{obj.service.duration} minutes'
        return '-'
    get_duration_display.short_description = 'Duration'
