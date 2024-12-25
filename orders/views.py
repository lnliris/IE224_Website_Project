from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart, CartItem
from .models import Order, OrderHistory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required(login_url='login')
def checkout(request):
    '''
    Hàm hiển thị thông tin hóa đơn và lưu hóa đơn

    Args:
        - request: người dùng (request.user), form hóa đơn (request.POST.get(...))

    Output:
        - Render form theo template checkout.html, lưu hóa đơn của người dùng nếu form đã nhập
    '''
    try:
        # Get the current cart using the session cart_id
        cart_id = _cart_id(request)
        cart = Cart.objects.get(cart_id=cart_id)

        # Retrieve user's cart items
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.error(request, "Không có sản phẩm nào trong giỏ hàng.")
            return redirect('cart')  # Redirect to cart if no items exist

        if request.method == "POST":
            # Gather data from the form
            name = request.POST.get("name")
            email = request.POST.get("email")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            mobile = request.POST.get("mobile")
            payment_method = request.POST.get("payment_method")

            # Create a new order
            order = Order.objects.create(
                user=request.user,
                cart=cart,
                status="processing",
            )

            # Save order history
            OrderHistory.objects.create(
                user=request.user,
                order=order,
                status="processing",
            )

            # Redirect to the order confirmation page
            messages.success(request, "Thanh toán thành công, đơn hàng của bạn đã được tạo!")
            return redirect('order_confirmation')

        # Calculate total cost and quantity
        total = sum(item.product.price * item.quantity for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total': total,
            'total_quantity': total_quantity,
        }

        return render(request, 'checkout.html', context)

    except Cart.DoesNotExist:
        return redirect('checkout')  # Redirect to checkout if cart does not exist
    except Exception as e:
        # Log the error for debugging
        print(f"Checkout error: {str(e)}")
        messages.error(request, "Đã xảy ra lỗi trong quá trình thanh toán.")
        return redirect('cart')  # Redirect to cart in case of error

# @login_required(login_url='login')
def order_confirmation(request):
    """
    Hàm hiển thị form confirm hóa đơn.
    """
    return render(request, 'order_confirmation.html')
    
def redirect_to_checkout_or_login(request):
    """
    Hàm điều hướng người dùng đến page checkout hoặc login
    """
    if request.user.is_authenticated:
        return redirect('checkout')
    return redirect('login')

def payment_view(request):
    """
    Hàm trả về payment view (phiên bản cũ của hàm checkout, không còn sử dụng)
    """
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

@login_required(login_url='login')
def order_history(request):
    """
    Hàm lấy lịch sử 
    """
    history = OrderHistory.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'order_history.html', {'history': history})


@login_required(login_url='login')
def order_detail(request, order_id):
    """
    Hàm hiển thị chi tiết hóa đơn
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})