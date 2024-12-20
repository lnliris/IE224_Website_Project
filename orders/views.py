from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from cart.models import Cart, CartItem
from .models import Order, OrderHistory
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    """Handle the checkout process and redirect to a confirmation page."""
    try:
        # Retrieve cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        if not cart_items.exists():
            return redirect('cart')  # Redirect if no items in the cart

        if request.method == "POST":
            # Create the order
            order = Order.objects.create(
                user=request.user,
                status="completed",
            )

            # Add order history
            OrderHistory.objects.create(
                user=request.user,
                order=order,
                status="completed",
            )

            # Redirect to confirmation page without order ID
            return redirect('order_confirmation')

        # Render checkout page
        total = sum(item.product.price * item.quantity for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)
        
        context = {
            'cart_items': cart_items,
            'total': total,
            'total_quantity': total_quantity,
        }
        return render(request, 'checkout.html', context)

    except Exception as e:
        return redirect('cart')  # Redirect to cart in case of errors

# @login_required
def order_confirmation(request):
    """Render a generic confirmation page."""
    return render(request, 'order_confirmation.html')
    
def redirect_to_checkout_or_login(request):
    """Redirect users to the checkout if logged in, or to login if not."""
    if request.user.is_authenticated:
        return redirect('checkout')  # Replace 'checkout' with the actual URL name for your checkout view
    return redirect('login')  # Replace 'login' with the actual URL name for your login view


def payment_view(request):
    """Handle payment view."""
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(cartitem__user=request.user).distinct().first()
        else:
            cart_id = request.session.get('cart_id')
            cart = get_object_or_404(Cart, id=cart_id)

        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if request.method == "POST":
            # Payment processing logic here
            # Example: Integrate with a payment gateway
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                cart=cart,
                status="completed",
            )

            OrderHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                order=order,
                status="completed",
            )

            # Mark cart items as inactive
            cart_items.update(is_active=False)

            return redirect('order_confirmation', order_id=order.id)

        context = {
            'cart_items': cart_items,
            'total': sum(item.product.price * item.quantity for item in cart_items),
        }
        return render(request, 'payment.html', context)

    except ObjectDoesNotExist:
        return redirect('checkout')


@login_required
def order_history(request):
    """Display the order history for the user."""
    history = OrderHistory.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'order_history.html', {'history': history})


@login_required
def order_detail(request, order_id):
    """Display detailed order information."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})