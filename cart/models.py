from django.db import models
from users.models import User
from products.models import Product, Variant
import uuid

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)  # Auto-created primary key
    cart_id = models.CharField(max_length=250, blank=True, unique=True)  # Unique identifier for cart
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the cart was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the cart was last updated

    def __str__(self):
        return str(self.cart_id)

class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)  # Auto-created primary key
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)  # Link to Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product
    variations = models.ManyToManyField(Variant, blank=True)  # Link to product variations
    is_active = models.BooleanField(default=True)  # Status of the cart item
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # Use custom user model

    def __str__(self):
        return str(self.product)

    def total_price(self):
        """Calculate the total price of the item (price * quantity)."""
        return self.product.price * self.quantity
