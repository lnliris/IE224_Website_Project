from django.db import models
from django.contrib.auth.models import User

# Model Danh mục sản phẩm
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Tên danh mục (ví dụ: Thời trang, Điện tử)
    description = models.TextField(null=True, blank=True)  # Mô tả danh mục

    def __str__(self):
        return self.name


# Model Sản phẩm
class Product(models.Model):
    name = models.CharField(max_length=200)  # Tên sản phẩm
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )  # Liên kết với danh mục
    price = models.FloatField()  # Giá sản phẩm
    description = models.TextField(null=True, blank=True)  # Mô tả sản phẩm
    image = models.ImageField(null=True, blank=True, upload_to='products/')  # Ảnh sản phẩm
    stock = models.PositiveIntegerField(default=0)  # Số lượng sản phẩm trong kho

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        """Kiểm tra xem sản phẩm còn hàng hay không"""
        return self.stock > 0
