from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Order, OrderHistory, Coupon
from cart.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    """Generate or retrieve the session cart ID."""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required
def order_summary(request):
    """Display a summary of the order."""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        order, created = Order.objects.get_or_create(user=request.user, cart=cart, status='in_progress')
        return render(request, 'order_summary.html', {'order': order})
    except Cart.DoesNotExist:
        return HttpResponse("No active cart found. Please add items to your cart.")


@login_required
def payment_view(request):
    """Handle payment view and context."""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        order = Order.objects.get(user=request.user, cart=cart, status='in_progress')
        context = {
            'order': order,
            'STRIPE_PUBLIC_KEY': 'your_stripe_public_key',  # Replace with your Stripe public key
        }
        return render(request, 'payment.html', context)
    except ObjectDoesNotExist:
        return HttpResponse("No active order found. Please checkout first.")


@login_required
def order_history(request):
    """Display the order history for the user."""
    history = OrderHistory.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'order_history.html', {'history': history})


@login_required
def checkout(request):
    """Handle the checkout process."""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        if not cart.items.exists():
            return render(request, 'checkout.html', {'error': 'Your cart is empty!'})

        order, created = Order.objects.get_or_create(user=request.user, cart=cart, status='in_progress')

        if request.method == 'POST':
            coupon_code = request.POST.get('coupon')
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    order.coupon = coupon
                    order.save()
                except Coupon.DoesNotExist:
                    return render(request, 'checkout.html', {'error': 'Invalid coupon code!'})

            # Mark cart items as ordered
            for item in cart.items.all():
                item.is_active = False
                item.save()

            # Redirect to payment
            return redirect('payment_view')

        return render(request, 'checkout.html', {'order': order})

    except Cart.DoesNotExist:
        return render(request, 'checkout.html', {'error': 'No cart found!'})


@login_required
def apply_coupon(request):
    """Apply a coupon to the current order."""
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            cart = Cart.objects.get(cart_id=_cart_id(request))
            order = Order.objects.get(user=request.user, cart=cart, status='in_progress')
            order.coupon = coupon
            order.save()
            return redirect('checkout')
        except Coupon.DoesNotExist:
            return HttpResponse("Invalid coupon code.")
        except Order.DoesNotExist:
            return HttpResponse("No active order found.")
