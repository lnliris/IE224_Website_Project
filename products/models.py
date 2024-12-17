from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Model Danh mục sản phẩm
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Tên danh mục (ví dụ: Thời trang, Điện tử)
    description = models.TextField(null=True, blank=True)  # Mô tả danh mục
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Tạo slug từ tên danh mục
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

    # Các trường ảnh phụ
    image_1 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Tự động tạo slug nếu chưa có
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    @property
    def formatted_price(self):
        return f"{self.price:,.0f} VND"
    @property
    def is_in_stock(self):
        """Kiểm tra xem sản phẩm còn hàng hay không"""
        return self.stock > 0

# Model Biến thể sản phẩm
class Variant(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ('Official', 'Chính hãng'),
        ('Pro', 'Pro'),
        ('Regular', 'Bình thường'),
    )

    MATERIAL_CHOICES = (
        ('Natural Rubber', 'Cao su tự nhiên'),
        ('Synthetic Rubber', 'Cao su nhân tạo'),
        ('EVA', 'EVA'),
        ('Carbon Fiber', 'Sợi carbon'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')  # Link to the product
    type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES, verbose_name="Loại sản phẩm")
    color = models.CharField(max_length=100)  # Variant value (e.g., Red, Green, Large, Small)
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, verbose_name="Chất liệu")

    def __str__(self):
        return f"{self.type}: {self.color} ({self.material}) - {self.product.name}"
    
0