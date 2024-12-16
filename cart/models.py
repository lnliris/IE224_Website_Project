from django.db import models
import uuid
from users.models import User
from products.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Thời điểm tạo giỏ hàng
    updated_at = models.DateTimeField(auto_now=True)  # Thời điểm cập nhật giỏ hàng gần nhất
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Cart of {self.user.username}, id: {self.cart_id}"

    # def total_items(self):
    #     """Tính tổng số lượng sản phẩm trong giỏ."""
    #     return sum(item.quantity for item in self.items.all())
    #
    # def update_total_price(self):
    #     """Tính tổng giá trị giỏ hàng."""
    #     return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items"
    )  # Liên kết với giỏ hàng
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # Liên kết với sản phẩm
    quantity = models.PositiveIntegerField(default=1)  # Số lượng sản phẩm trong giỏ
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"

    def total_price(self):
        """Tính tổng giá của item (price * quantity)."""
        return self.product.price * self.quantity
