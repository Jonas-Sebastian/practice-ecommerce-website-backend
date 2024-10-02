from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, CreditCardPayment, PayPalPayment, BankTransferPayment, GCashPayment, MayaPayment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Only accept category ID

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Accepts just the product ID

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'shipping_address', 
                  'order_notes', 'payment_method', 'created_at', 'status', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
        
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