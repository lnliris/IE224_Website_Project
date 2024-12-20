from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart, CartItem
from .models import Order, OrderHistory
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required(login_url='login')

def checkout(request):
    cart_id1= request.session.get('cart_id')
    print(cart_id1)
    try:
        # Lấy thông tin giỏ hàng của người dùng
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, "Không có sản phẩm nào trong giỏ hàng.")
            return redirect('cart')  # Quay lại giỏ hàng nếu không có sản phẩm
        if request.method == "POST":
            # Lấy dữ liệu từ form
            name = request.POST.get("name")
            email = request.POST.get("email")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            mobile = request.POST.get("mobile")
            payment_method = request.POST.get("payment_method")
            cart_id=_cart_id(request)
            print(request.user)  # Thông báo khi nhận POST
            print(cart_id)  # Thông báo khi nhận POST
            if Cart.objects.filter(cart_id=cart_id).exists():
                print(cart_id) 
                cart = Cart.objects.get(cart_id=cart_id)
            else:
                print(cart_id) 
                print("check không")
                new_cart_id = str(uuid.uuid4())  # Tạo UUID mới
                request.session['cart_id'] = new_cart_id  # Lưu vào session
                cart = Cart.objects.create(cart_id=new_cart_id)
            # print(cart)  # Thông báo khi nhận POST
            # Tạo đơn hàng
            print("check")
            order = Order.objects.create(
                user=request.user,
                cart=cart,
                status="processing",
            )

            # Cập nhật trạng thái giỏ hàng (vô hiệu hóa)
            cart.save()

            # Lưu lịch sử đơn hàng
            OrderHistory.objects.create(
                user=request.user,
                order=order,
                status="processing",
            )

            new_cart_id = str(uuid.uuid4())  # Tạo UUID mới
            request.session['cart_id'] = new_cart_id  # Lưu vào session
            
            # Tạo một giỏ hàng mới trong cơ sở dữ liệu
            Cart.objects.create(cart_id=new_cart_id)
            cart_items.delete()
            print("Nhận Thông tin 2")  # Thông báo khi nhận POST
            # Chuyển hướng đến trang xác nhận
            return redirect('order_confirmation')

        # Tính tổng giá trị đơn hàng
        total = sum(item.product.price * item.quantity for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)


        # Render trang checkout
        context = {
            'cart_items': cart_items,
            'total': total,
            'total_quantity': total_quantity,
        }

        return render(request, 'checkout.html', context)

    except Exception as e:
        messages.error(request, "Đã xảy ra lỗi trong quá trình thanh toán.")
        return redirect('cart')  # Quay lại giỏ hàng trong trường hợp lỗi


# @login_required(login_url='login')
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


@login_required(login_url='login')
def order_history(request):
    """Display the order history for the user."""
    history = OrderHistory.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'order_history.html', {'history': history})


@login_required(login_url='login')
def order_detail(request, order_id):
    """Display detailed order information."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})