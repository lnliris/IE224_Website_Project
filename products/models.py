from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Model Danh mục sản phẩm
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Tên danh mục (ví dụ: Thời trang, Điện tử)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Tạo slug từ tên danh mục
    description = models.TextField(null=True, blank=True)  # Mô tả danh mục

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Tự động tạo slug nếu chưa có
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# Model Sản phẩm
class Product(models.Model):
    name = models.CharField(max_length=200)  # Tên sản phẩm
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Tạo slug từ tên sản phẩm
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )  # Liên kết với danh mục
    price = models.FloatField()  # Giá sản phẩm
    description = models.TextField(null=True, blank=True)  # Mô tả sản phẩm
    image = models.ImageField(null=True, blank=True, upload_to='products/')  # Ảnh sản phẩm
    stock = models.PositiveIntegerField(default=0)  # Số lượng sản phẩm trong kho

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Tự động tạo slug nếu chưa có
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        """Kiểm tra xem sản phẩm còn hàng hay không"""
        return self.stock > 0


# Model Biến thể sản phẩm
class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')  # Liên kết với sản phẩm
    name = models.CharField(max_length=100)  # Tên biến thể (ví dụ: Màu sắc, Kích thước)
    value = models.CharField(max_length=100)  # Giá trị của biến thể (ví dụ: Đỏ, Xanh, Lớn, Nhỏ)
    stock = models.PositiveIntegerField(default=0)  # Số lượng sản phẩm trong kho cho biến thể

    def __str__(self):
        return f"{self.name}: {self.value} ({self.product.name})"

    @property
    def is_in_stock(self):
        """Kiểm tra xem biến thể còn hàng hay không"""
        return self.stock > 0
