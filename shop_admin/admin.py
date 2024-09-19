from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import ShopAdminAccount

@admin.register(ShopAdminAccount)
class ShopAdminAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_admin', 'created_at', 'updated_at')
    list_filter = ('is_staff', 'is_admin')
    search_fields = ('email', 'username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_admin')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Ensure password is hashed before saving
        if form.cleaned_data['password']:
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
