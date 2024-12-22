from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Variant
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from orders.models import Order
import uuid

def _cart_id(request):
    if request.user.is_authenticated:
        # For authenticated users, get the cart linked to the user
        cart = Cart.objects.filter(user=request.user).exclude(id__in=Order.objects.values_list('cart_id', flat=True)).first()
        if not cart:
            cart_id = str(uuid.uuid4())
            cart = Cart.objects.create(cart_id=cart_id, user=request.user)
    else:
        # For guests, use the cart_id stored in session or create a new one
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart_id = str(uuid.uuid4())
            request.session['cart_id'] = cart_id
            cart = Cart.objects.create(cart_id=cart_id)  # Ensure cart creation for guests
        else:
            cart = get_object_or_404(Cart, cart_id=cart_id)

    return cart.cart_id

def merge_cart_items(request):
    """
    Merge items from the session cart into the user's cart after login.
    The user now controls the cart, and items are linked via the cart.
    """
    # Get the user's cart using _cart_id(request)
    cart_id = _cart_id(request)

    # Access session cart
    session_cart_id = request.session.get('cart_id')
    session_cart = Cart.objects.filter(cart_id=session_cart_id).first()

    if session_cart:
        # Get or create the user's cart using cart_id
        user_cart, created = Cart.objects.get_or_create(cart_id=cart_id, user = request.user)
        print(f"User Cart: {user_cart}, Created: {created}")  # Debug statement

        # Iterate through session cart items
        for session_item in session_cart.cart_items.all():
            # Directly associate session item with user cart
            session_item.cart = user_cart
            session_item.save()
            print(f"Added Item: {session_item.product}, Quantity: {session_item.quantity}")  # Debug statement

        # Delete the session cart
        session_cart.delete()
        request.session.pop('cart_id', None)  # Remove the session cart_id

    return None  # Removed the return statement


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)

    # Get or create the cart
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(cart_id=cart_id, user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    # Add or update the cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,  # Ensure the cart is set here
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)

    # Get the cart and cart item
    if request.user.is_authenticated:
        cart_item = get_object_or_404(
            CartItem, 
            cart__user=request.user, 
            cart__cart_id=cart_id, 
            product=product, 
            id=cart_item_id
        )
    else:
        cart = get_object_or_404(Cart, cart_id=cart_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product, id=cart_item_id)

    # Decrease quantity or delete the item
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)

    # Get the cart and cart item
    if request.user.is_authenticated:
        cart_item = get_object_or_404(
            CartItem, 
            cart__user=request.user, 
            cart__cart_id=cart_id, 
            product=product, 
            id=cart_item_id
        )
    else:
        cart = get_object_or_404(Cart, cart_id=cart_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')

def cart(request):
    total = 0
    quantity = 0
    cart_items = []

    try:
        cart_id = _cart_id(request)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                cart__user=request.user, 
                cart__cart_id=cart_id, 
                is_active=True
            )
        else:
            cart = get_object_or_404(Cart, cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Calculate total and quantity
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass  # Ignore missing cart

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

