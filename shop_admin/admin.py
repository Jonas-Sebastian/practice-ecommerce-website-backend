from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import ShopAdminAccount

@admin.register(ShopAdminAccount)
class ShopAdminAccountAdmin(admin.ModelAdmin):
    list_display = ('display_id', 'email', 'username', 'is_staff', 'is_admin', 'created_at', 'updated_at', 'is_approved')
    list_filter = ('is_staff', 'is_admin', 'is_approved')
    search_fields = ('email', 'username')
    readonly_fields = ('created_at', 'updated_at', 'password')
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_admin', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )