from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Variant
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import uuid

# Create your views here.

def get_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    return cart

def _cart_id(request):
    cart_id = request.POST.get('cart_id') or request.session.get('cart_id')

    if cart_id:
        try:
            uuid.UUID(cart_id)  # Validate that cart_id is a valid UUID
        except (ValueError, TypeError):
            cart_id = str(uuid.uuid4())  # Invalid UUID, create a new one
            request.session['cart_id'] = cart_id
    else:
        cart_id = str(uuid.uuid4())  # Generate a new UUID if none exists
        request.session['cart_id'] = cart_id

    return cart_id

def merge_cart_items(user, session_cart):
    """Merge session cart items into the user's cart after login."""
    user_cart_items = CartItem.objects.filter(user=user)
    for session_item in session_cart:
        matching_items = user_cart_items.filter(product=session_item.product, variations__in=session_item.variations.all())
        if matching_items.exists():
            user_item = matching_items.first()
            user_item.quantity += session_item.quantity
            user_item.save()
        else:
            session_item.user = user
            session_item.cart = None
            session_item.save()
    session_cart.delete()

def add_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    current_user = request.user
    product = Product.objects.get(id=product_id) 
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variant.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    if current_user.is_authenticated:
        # Merge session cart items into user's cart if applicable
        session_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request))
        if session_cart.exists():
            merge_cart_items(current_user, session_cart)

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # Tăng số lượng
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(
                    product=product, 
                    quantity=1, 
                    user=current_user,
                )
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # lấy cart 
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    """Giảm số sản phẩm trong giỏ hàng"""
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    """Xóa hoàn toàn sản phẩm ra khỏi giỏ hàng"""
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            # Merge session cart items into user's cart after login
            session_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request))
            if session_cart.exists():
                merge_cart_items(request.user, session_cart)

            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)
