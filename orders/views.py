from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Order, OrderHistory, Coupon
from cart.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import uuid

def _cart_id(request):
    """Generate or validate a session cart ID."""
    cart_id = request.session.get('cart_id')  # Retrieve existing cart_id from session

    try:
        # Validate that cart_id is a valid UUID
        uuid.UUID(cart_id)
    except (ValueError, TypeError):
        # If invalid, generate a new UUID and store it in the session
        cart_id = str(uuid.uuid4())
        request.session['cart_id'] = cart_id

    return cart_id



# @login_required
# def order_summary(request):
#     """Display a summary of the order."""
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         order, created = Order.objects.get_or_create(user=request.user, cart=cart, status='in_progress')
#         return render(request, 'order_summary.html', {'order': order})
#     except Cart.DoesNotExist:
#         return HttpResponse("No active cart found. Please add items to your cart.")


@login_required
def payment_view(request):
    """Handle payment view and context."""
    try:
        # Retrieve the cart and associated order
        cart = Cart.objects.get(cart_id=_cart_id(request))
        order = Order.objects.get(user=request.user, cart=cart, status='in_progress')

        context = {
            'order': order,  # Pass order details to the template
        }
        return render(request, 'payment.html', context)
    except ObjectDoesNotExist:
        # Redirect back to checkout with an error message
        return redirect('/orders/checkout/?error=No active order found. Please checkout first.')


@login_required
def order_history(request):
    """Display the order history for the user."""
    history = OrderHistory.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'order_history.html', {'history': history})


@login_required
@login_required
def checkout(request):
    """Handle the checkout process."""
    try:
        # Attempt to retrieve the cart and associated order
        cart = Cart.objects.get(cart_id=_cart_id(request))
        order, created = Order.objects.get_or_create(user=request.user, cart=cart, status='in_progress')

        # Pass the order context to the template
        context = {
            'order': order,
            'error_message': None,  # No error by default
        }
        return render(request, 'checkout.html', context)

    except ObjectDoesNotExist:
        # Handle missing cart or order by adding an error message
        context = {
            'order': None,
            'error_message': "No active order found. Please add items to your cart and proceed to checkout.",
        }
        return render(request, 'checkout.html', context)


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
