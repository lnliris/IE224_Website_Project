from django.db import models
import uuid
from users.models import User
from products.models import Product, Variant

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)  # Thời điểm tạo giỏ hàng
    updated_at = models.DateTimeField(auto_now=True)  # Thời điểm cập nhật giỏ hàng gần nhất
   

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) #Liên kết với user
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=False, blank=False, related_name="items"
    )  # Liên kết với giỏ hàng
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # Liên kết với sản phẩm
    quantity = models.PositiveIntegerField(default=1) 
    variations = models.ManyToManyField(Variant, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.price
    
    def total_price(self):
        """Tính tổng giá của item (price * quantity)."""
        return self.product.price * self.quantity
