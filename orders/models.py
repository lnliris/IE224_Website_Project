from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product

class Coupon(models.Model):
    '''
    Lớp quản lý các mã giảm giá (nhóm chưa triển khai)
    '''
    code = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Coupon {self.code} - {self.amount}"


class Order(models.Model):
    '''
    Lớp quản lý các hóa đơn người dùng
    '''
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.OneToOneField('cart.Cart', on_delete=models.CASCADE)  
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    ordered_date = models.DateTimeField(default=timezone.now)

    def get_total(self):
        '''
        Hàm lấy tổng giá trị đơn hàng

        Output:
            - Tổng giá trị của đơn hàng
        '''
        total = sum(item.total_price() for item in self.cart.items.all())
        if self.coupon:
            total -= self.coupon.amount
        return total

    def mark_as_completed(self):
        '''
        Hàm đánh dấu đơn hàng đã hoàn thành (người dùng đã nhận được)
        '''
        self.status = 'completed'
        self.save()
        OrderHistory.objects.create(user=self.user, order=self, status='completed')
class OrderHistory(models.Model):
    '''
    Lớp quản lý lịch sử đơn hàng
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order.id} - {self.status} - {self.updated_at}"
