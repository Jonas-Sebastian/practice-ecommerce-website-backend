from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No extra empty forms

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_id', 'customer_name', 'customer_email', 'shipping_address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'shipping_address')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)  # Show latest orders first

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_id', 'name', 'description')  # Include display_id in list_display
    search_fields = ('name',)  # Allow searching by category name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_id', 'name', 'category', 'price', 'stock', 'available')  # Include display_id
    list_filter = ('category', 'available')  # Filter by category and availability
    search_fields = ('name', 'category__name')  # Search by product name and category name
