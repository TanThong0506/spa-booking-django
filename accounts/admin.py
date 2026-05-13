from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'get_email')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('get_email',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'get_email')
        }),
        ('Profile Details', {
            'fields': ('role', 'phone')
        }),
    )

    def get_email(self, obj):
        return obj.user.email if obj.user else '-'
    get_email.short_description = 'Email'