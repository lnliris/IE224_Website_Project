from django.shortcuts import render, redirect, get_object_or_404
# from orders.views import order_summary
from products.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import uuid

# Create your views here.

def _cart_id(request):
    """Tạo hoặc lấy session ID cho người dùng"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    current_user = request.user
    product = Product.objects.get(id = product_id) # Lấy sản phẩm từ Product bằng product_id

    if not product.is_in_stock:
        return HttpResponse("Sản phẩm hiện không còn hàng.")

    if current_user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product = product,
            user = current_user,
            defaults = {'quantity': 1}
        )
        if not created:
            if product.stock >= cart_item.quantity + 1:
                cart_item.quantity += 1
                cart_item.save()
            else:
                return HttpResponse("Không đủ hàng để thêm vào giỏ.")
            return redirect('cart')

    else:
        # return redirect('login')
        cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            defaults={'quantity': 1}
        )
        if not created:
            if product.stock >= cart_item.quantity + 1:
                cart_item.quantity += 1
                cart_item.save()
            else:
                return HttpResponse("Không đủ hàng để thêm vào giỏ.")
        return redirect('cart')

def remove_from_cart(request, product_id, cart_item_id):
    """Giảm số lượng sản phẩm hoặc xóa nếu quantity=1"""
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
    """Hiển thị nội dung giỏ hàng"""
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            total += item.total_price()
            quantity += item.quantity

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }

    return render(request, 'cart.html', context)


# @login_required(login_url='login')
# def checkout(request, total=0, quantity=0, cart_items=None):
#     """Hiển thị thông tin thành toán"""
#     try:
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)

#         for item in cart_items:
#             total += item.total_price()
#             quantity += item.quantity

#     except ObjectDoesNotExist:
#         pass

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#     }
#     return render(request, 'order_summary.html', context)