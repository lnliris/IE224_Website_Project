
from django.shortcuts import render
from .models import Order, OrderHistory
from cart import models, views
from cart.models import Cart, CartItem 

def order_summary(request):
    order = Order.objects.get(user=request.user, ordered=False)
    return render(request, 'order_summary.html', {'object': order})

def payment_view(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'order': order,
        'STRIPE_PUBLIC_KEY': 'your_stripe_public_key',
    }
    return render(request, 'payment.html', context)

def order_history(request):
    history = OrderHistory.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'order_history.html', {'history': history})

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)