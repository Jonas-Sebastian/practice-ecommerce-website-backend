from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No extra empty forms

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'shipping_address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'shipping_address')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)  # Show latest orders first

admin.site.register(Category)
admin.site.register(Product)
