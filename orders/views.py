from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from cart.models import Cart, CartItem
from .models import Order, OrderHistory
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.contrib.auth.decorators import login_required

# def _cart_id(request):
#     """Retrieve or create a session cart ID."""
#     cart_id = request.session.get('cart_id')
#     if not cart_id:
#         cart_id = str(uuid.uuid4())
#         request.session['cart_id'] = cart_id
#     return cart_id


def checkout(request):
    """Handle the checkout process for logged-in and non-logged-in users."""
    try:
        # Use the existing cart ID to retrieve the cart
        if request.user.is_authenticated:
            cart = Cart.objects.filter(cartitem__user=request.user).distinct().first()
        else:
            cart_id = request.session.get('cart_id')
            cart = get_object_or_404(Cart, id=cart_id)

        if not cart:
            raise Cart.DoesNotExist

        # Create or retrieve an order linked to the cart
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(
                cart=cart,
                defaults={'user': request.user, 'status': 'in_progress'}
            )
        else:
            order, created = Order.objects.get_or_create(cart=cart, defaults={'status': 'in_progress'})

        context = {
            'order': order,
            'error_message': None,
        }
        return render(request, 'checkout.html', context)

    except Cart.DoesNotExist:
        context = {
            'order': None,
            'error_message': "No active cart found. Please add items to your cart and try again.",
        }
        return render(request, 'checkout.html', context)


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


def order_confirmation(request, order_id):
    """Display confirmation page after successful payment."""
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'order_confirmation.html', context)


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