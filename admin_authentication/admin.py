from django.contrib import admin
from .models import ShopAdminAccount

class ShopAdminAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    filter_horizontal = ('user_permissions', 'groups')

    exclude = ('last_login',)
admin.site.register(ShopAdminAccount, ShopAdminAccountAdmin)