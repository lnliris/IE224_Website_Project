from django.urls import path
from .views import ProductsView
from . import views
urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'), 
    # path('products/', ProductsView.as_view(), name='products'),
    path('', views.product_list, name='product_list'),  # Danh sách sản phẩm
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),  # Theo danh mục
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),  # Chi tiết sản phẩm
]