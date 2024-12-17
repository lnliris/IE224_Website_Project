from django.urls import path
from .views import ProductsView, product_detail, product_list, index


urlpatterns = [
    path('', ProductsView.as_view(), name='products'),  # Trang danh sách sản phẩm
    path('products/<slug:product_slug>/', product_detail, name='product_detail'),  # Trang chi tiết sản phẩm
    path('category/<slug:category_slug>/', product_list, name='product_list_by_category'),  # Lọc sản phẩm theo danh mục
]