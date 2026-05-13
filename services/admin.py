from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active', 'created_at', 'get_status_display')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'get_formatted_price')
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'get_formatted_price', 'duration')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_status_display(self, obj):
        if obj.is_active:
            return '✅ Active'
        return '❌ Inactive'
    get_status_display.short_description = 'Status'

    def get_formatted_price(self, obj):
        return f'{obj.price:,.0f} VND' if obj.price else '-'
    get_formatted_price.short_description = 'Formatted Price'