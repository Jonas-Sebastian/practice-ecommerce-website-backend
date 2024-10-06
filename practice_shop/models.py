from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    display_id = models.IntegerField(unique=True, editable=False, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only set display_id for new instances
            max_display_id = Category.objects.aggregate(models.Max('display_id'))['display_id__max']
            self.display_id = (max_display_id or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.BigIntegerField(default=0)
    available = models.BooleanField(default=True)
    display_id = models.IntegerField(unique=True, editable=False, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only set display_id for new instances
            max_display_id = Product.objects.aggregate(models.Max('display_id'))['display_id__max']
            self.display_id = (max_display_id or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('gcash', 'GCash'),
        ('maya', 'Maya'),
        ('cod', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('returned', 'Returned'),
        ('failed', 'Failed'),
        ('on_hold', 'On Hold'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=254)
    shipping_address = models.TextField(blank=True, null=True)
    order_notes = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cod')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    display_id = models.IntegerField(unique=True, editable=False, null=True)

    products = models.ManyToManyField(Product, through='OrderItem')

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only set display_id for new instances
            max_display_id = Order.objects.aggregate(models.Max('display_id'))['display_id__max']
            self.display_id = (max_display_id or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.display_id} by {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.display_id}"

class PaymentDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class CreditCardPayment(PaymentDetails):
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # Format: MM/YY
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Credit Card Payment for Order {self.order.display_id}"

class PayPalPayment(PaymentDetails):
    paypal_email = models.EmailField()

    def __str__(self):
        return f"PayPal Payment for Order {self.order.display_id}"

class BankTransferPayment(PaymentDetails):
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Bank Transfer Payment for Order {self.order.display_id}"

class GCashPayment(PaymentDetails):
    def __str__(self):
        return f"GCash Payment for Order {self.order.display_id}"

class MayaPayment(PaymentDetails):
    def __str__(self):
        return f"Maya Payment for Order {self.order.display_id}"
