from django.contrib import admin

# Register your models here.
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)