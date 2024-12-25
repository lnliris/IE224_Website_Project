from django.db import models
from users.models import User
from products.models import Product
import uuid

class Cart(models.Model):
    '''
    Lớp quản lý giỏ hàng
    '''
    cart_id = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.cart_id

    @property
    def items(self):
        # Return related CartItems
        return self.cart_items.all()

class CartItem(models.Model):
    '''
    Lớp quản lý các sản phẩm trong giỏ hàng
    '''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')  # Liên kết với giỏ hàng
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Liên kết với sản phẩm
    quantity = models.PositiveIntegerField(default=1) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

    def total_price(self):
        """Tính tổng giá của item (price * quantity)."""
        return self.product.price * self.quantity

