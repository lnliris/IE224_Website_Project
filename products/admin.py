from django.contrib import admin
from .models import *



class InStockFilter(admin.SimpleListFilter):
    title = 'Còn hàng'
    parameter_name = 'in_stock'
    def lookups(self, request, model_admin):
        return [
            ('yes', 'Còn hàng'),
            ('no', 'Hết hàng'),
        ]
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(stock__gt=0)
        if self.value() == 'no':
            return queryset.filter(stock__lte=0)
        return queryset
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_in_stock', 'slug')
    list_filter = ('category', InStockFilter)  # Sử dụng bộ lọc tùy chỉnh
    prepopulated_fields = {'slug': ('name',)}
    def is_in_stock(self, obj):
        return obj.stock > 0
    is_in_stock.boolean = True  # Hiển thị icon đúng/sai
    is_in_stock.short_description = 'Còn hàng'


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('type', 'color', 'material', 'product_name')

    def product_name(self, obj):
        return obj.product.name  # Hiển thị tên sản phẩm từ model `Product`
    product_name.short_description = 'Sản phẩm'  # Đặt tiêu đề cột

    def is_in_stock(self, obj):
        return obj.is_in_stock  # Hiển thị thông tin về việc còn hàng
    is_in_stock.short_description = 'Còn hàng'