from django.contrib import admin
from .models import WaitlistEntry

@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'location', 'role', 'created_at')
    search_fields = ('full_name', 'email', 'location')
    list_filter = ('role', 'created_at', 'is_active')
    readonly_fields = ('created_at',)