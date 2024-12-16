from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<product_id>/', views.add_cart, name='add_cart'),
    path('remove/<product_id>/<cart_item_id>/', views.remove_from_cart, name='remove_cart'),
    path('remove_item/<product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
]