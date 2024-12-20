from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Coupon {self.code} - {self.amount}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.OneToOneField('cart.Cart', on_delete=models.CASCADE)  # Link to the cart
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    ordered_date = models.DateTimeField(default=timezone.now)

    def get_total(self):
        total = sum(item.total_price() for item in self.cart.items.all())
        if self.coupon:
            total -= self.coupon.amount
        return total

    def mark_as_completed(self):
        self.status = 'completed'
        self.save()
        OrderHistory.objects.create(user=self.user, order=self, status='completed')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class OrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order.id} - {self.status} - {self.updated_at}"
