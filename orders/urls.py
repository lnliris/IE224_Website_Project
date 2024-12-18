from django.urls import path
from . import views

urlpatterns = [
    # path('order-summary/', views.order_summary, name='order-summary'),
    path('payment/', views.payment_view, name='payment'),
    path('order-history/', views.order_history, name='order-history'),
    path('checkout/', views.checkout, name='checkout'),
]