from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

# Create your models here.
ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
]

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    ordered_date = models.DateTimeField(default=timezone.now)

    def get_total(self):
        total = sum([item.get_total_item_price() for item in self.items.all()])
        if self.coupon:
            total -= self.coupon.amount
        return total

    def mark_as_completed(self):
        self.status = 'completed'
        self.save()
        OrderHistory.objects.create(user=self.user, order=self, status='completed')
    
class OrderHistory(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order.id} - {self.status} - {self.updated_at}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Mã coupon
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Số tiền giảm giá

    def __str__(self):
        return f"Coupon {self.code} - {self.amount}"

