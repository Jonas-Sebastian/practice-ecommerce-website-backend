from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, CreditCardPayment, PayPalPayment, BankTransferPayment, GCashPayment, MayaPayment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'display_id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Accepts category ID

    class Meta:
        model = Product
        fields = ['id', 'display_id', 'name', 'category', 'description', 'price', 'image', 'stock', 'available']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='display_id'
    )
    product_name = serializers.ReadOnlyField(source='product.name')
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'product_image', 'quantity', 'price']

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    status_choices = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'display_id', 'customer_name', 'customer_email', 'shipping_address', 
                  'order_notes', 'payment_method', 'created_at', 'status', 'order_items', 'status_choices']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
    
    def get_status_choices(self, obj):
        return Order.STATUS_CHOICES
        
class CreditCardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardPayment
        fields = ['order', 'card_number', 'expiry_date', 'cvv']

class PayPalPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalPayment
        fields = ['order', 'paypal_email']

class BankTransferPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransferPayment
        fields = ['order', 'account_name', 'account_number', 'bank_name']

class GCashPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCashPayment
        fields = ['order']

class MayaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MayaPayment
        fields = ['order']