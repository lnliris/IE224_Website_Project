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
    '''
    Hàm tạo id cho cart

    Args:
        - request (dict): request.user là người dùng sở hữu cart, request.session['cart_id] là cart tạm thời

    Output:
        - cart.cart_id: id của cart đã tạo ra nếu người dùng chưa đăng nhập, id của cart người dùng nếu đã đăng nhập
    '''
    if request.user.is_authenticated:
        # Truy vấn cart của người dùng (nằm trong list cart của người dùng nhưng ko nằm trong order)
        cart = Cart.objects.filter(user=request.user).exclude(id__in=Order.objects.values_list('cart_id', flat=True)).first()

        # Nếu không tìm thấy thì tạo ra cart mới
        if not cart: 
            cart_id = str(uuid.uuid4())
            cart = Cart.objects.create(cart_id=cart_id, user=request.user)
    else:
        # Với khách, lấy session.cart_id hoặc tạo ra cart mới
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
    Hàm merge cart tạm thời với cart của người dùng

    Args:
        - request (dict): request.user là người dùng hiện tại, request.session['cart_id] là cart tạm thời

    """
    # Lấy hoặc tạo ra cart_id cho người dùng
    cart_id = _cart_id(request)

    # Lấy session cart
    session_cart_id = request.session.get('cart_id')
    session_cart = Cart.objects.filter(cart_id=session_cart_id).first()

    if session_cart:
        # Lấy cart
        user_cart, created = Cart.objects.get_or_create(cart_id=cart_id, user = request.user)

        # Merge các phần tử của hai cart
        for session_item in session_cart.cart_items.all():
            # Directly associate session item with user cart
            session_item.cart = user_cart
            session_item.save()

        # Xóa session cart
        session_cart.delete()
        request.session.pop('cart_id', None)

    return None

def add_cart(request, product_id):
    '''
    Hàm thêm sản phẩm vào cart

    Args:
        - request (dict): request.user là người dùng hiện tại
        - product_id (str): mã sản phẩm

    Output:
        - Cập nhật giỏ hàng và chuyển hướng đến url cart
    '''
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)

    # Lấy hoặc tạo cart
    if request.user.is_authenticated: # Trường hợp người dùng đã đăng nhập
        cart, _ = Cart.objects.get_or_create(cart_id=cart_id, user=request.user)
    else: # Trường hợp chưa đăng nhập
        cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    # Tạo các cart_item chưa có trong giỏ hàng
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,  # Ensure the cart is set here
        product=product,
        defaults={'quantity': 1}
    )
    # Cập nhật số lượng nếu đã có trong giỏ hàng
    if not created: 
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    '''
    Hàm giảm số lượng sản phẩm đi một

    Args:
        - request (dict): request.user là người dùng hiện tại
        - product_id: mã sản phẩm muốn thay đổi.
        - cart_item_id: mã của sản phẩm trong giỏ hàng 

    Output: 
        - Giảm số lượng sản phẩm đã chọn đi một, nếu về 0 thì xóa khỏi giỏ hàng. Sau đó điều hướng đến url cart
    '''
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)

    # Lấy cart và cart_item
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

    # Giảm số lượng hoặc xóa sản phẩm
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    '''
    Hàm xóa một sản phẩm khỏi giỏ hàng

    Args:
        - request (dict): request.user là người dùng hiện tại
        - product_id: mã sản phẩm muốn thay đổi.
        - cart_item_id: mã của sản phẩm trong giỏ hàng 

    Output: 
        - Xóa sản phẩm khỏi giỏ hàng rồi điều hướng đến url cart
    '''

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
    '''
    Hàm hiển thị các sản phẩm trong cart

    Args:
        - request (dict): request.user là người dùng hiện tại.
    
    Output:
        - render các sản phẩm trong giỏ hàng theo template cart.html 
    '''
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

        # Tính tổng giá trị của giỏ hàng và số lượng các sản phẩm.
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

