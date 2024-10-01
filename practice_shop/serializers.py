from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, CreditCardPayment, PayPalPayment, BankTransferPayment, GCashPayment, MayaPayment

# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializer for the OrderItem model
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'product_id', 'quantity', 'price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('product_id', None)
        return representation

# Serializer for Order creation, which includes payment details and order items
class OrderCreateSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)
    payment_method_data = serializers.JSONField(write_only=True)  # Add this field to handle payment method data

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_email',
            'shipping_address',
            'order_notes',
            'payment_method',
            'payment_method_data',  # Add payment_method_data here
            'products',
        ]

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        payment_method_data = validated_data.pop('payment_method_data')

        # Create the order
        order = Order.objects.create(**validated_data)

        # Create order items
        for product_data in products_data:
            product = product_data.get('product')
            OrderItem.objects.create(order=order, product=product, quantity=product_data['quantity'], price=product_data['price'])

        # Handle different payment methods
        payment_method = validated_data.get('payment_method')

        # Credit Card Payment
        if payment_method == 'credit_card':
            CreditCardPayment.objects.create(
                order=order,
                card_number=payment_method_data['card_number'],
                expiry_date=payment_method_data['expiry_date'],
                cvv=payment_method_data['cvv']
            )

        # PayPal Payment
        elif payment_method == 'paypal':
            PayPalPayment.objects.create(
                order=order,
                paypal_email=payment_method_data['paypal_email']
            )

        # Bank Transfer Payment
        elif payment_method == 'bank_transfer':
            BankTransferPayment.objects.create(
                order=order,
                account_name=payment_method_data['account_name'],
                account_number=payment_method_data['account_number'],
                bank_name=payment_method_data['bank_name']
            )

        # GCash Payment
        elif payment_method == 'gcash':
            GCashPayment.objects.create(order=order)

        # Maya Payment
        elif payment_method == 'maya':
            MayaPayment.objects.create(order=order)

        return order