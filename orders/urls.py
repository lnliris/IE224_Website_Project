from django.urls import path
from . import views

urlpatterns = [
    # path('order-summary/', views.order_summary, name='order-summary'),
    path('payment/', views.payment_view, name='payment'),
    path('order-history/', views.order_history, name='order-history'),
    path('checkout/', views.redirect_to_checkout_or_login, name='redirect_checkout'),
    path('checkout/process/', views.checkout, name='checkout'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),  # For detailed order view
    ]