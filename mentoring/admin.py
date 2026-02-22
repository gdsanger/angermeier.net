from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'role', 'status', 'created_at']
    list_filter = ['status', 'role']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at']
