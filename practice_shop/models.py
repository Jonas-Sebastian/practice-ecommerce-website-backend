from django.db import models

# Category model to represent product categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Product model to represent items for sale
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} {self.name}"

# Order model to represent customer orders
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    shipping_address = models.TextField(null=True)
    order_notes = models.TextField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=50, 
        choices=[
            ('credit_card', 'Credit Card'), 
            ('paypal', 'PayPal'), 
            ('bank_transfer', 'Bank Transfer'),
            ('gcash', 'GCash'),
            ('maya', 'Maya'),
            ('cod', 'Cash on Delivery'),
        ],
        default='cod'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('out_for_delivery', 'Out for Delivery'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
            ('refunded', 'Refunded'),
            ('returned', 'Returned'),
            ('failed', 'Failed'),
            ('on_hold', 'On Hold')
        ],
        default='pending'
    )

    products = models.ManyToManyField(Product, through='OrderItem')

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

# OrderItem model to represent the relationship between Orders and Products (with quantity and price)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# Abstract model to handle payment details
class PaymentDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    class Meta:
        abstract = True

# Credit Card payment model
class CreditCardPayment(PaymentDetails):
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # Format: MM/YY
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Credit Card Payment for Order {self.order.id}"

# PayPal payment model
class PayPalPayment(PaymentDetails):
    paypal_email = models.EmailField()

    def __str__(self):
        return f"PayPal Payment for Order {self.order.id}"

# Bank Transfer payment model
class BankTransferPayment(PaymentDetails):
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Bank Transfer Payment for Order {self.order.id}"

# GCash payment model (you mentioned using QR codes, so only the order reference is kept)
class GCashPayment(PaymentDetails):
    def __str__(self):
        return f"GCash Payment for Order {self.order.id}"

# Maya payment model (QR code-based as well)
class MayaPayment(PaymentDetails):
    def __str__(self):
        return f"Maya Payment for Order {self.order.id}"
