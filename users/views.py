from django.shortcuts import render, redirect
from .forms import RegisterForms, LoginForms, ProfileUpdateForm
from django.contrib.auth import authenticate as default_authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from cart.views import _cart_id, merge_cart_items
from cart.models import CartItem

User = get_user_model()

def authenticate(username=None, password=None):
    if username and password:
        try:
            # Check for either username or email
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
    return None

def register_view(request):
    success_message = ""
    error_message = ""

    if request.method == 'POST':
        form = RegisterForms(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                )
                user.save()
                success_message = "Registration successful! You can now log in."
                login(request, user)
                merge_cart_items(request)
                next_url = request.session.pop('next', 'profile')
                return redirect(next_url)

            except Exception as e:
                error_message = f"Error: {str(e)}"
        else:
            error_message = "Invalid form submission. Please check your input."

    else:
        form = RegisterForms()

    return render(request, 'register.html', {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    })
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                merge_cart_items(request)
                next_url = request.session.pop('next', 'profile')
                return redirect(next_url)
            else:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        # Save the next URL if coming from another page
        next_url = request.GET.get('next', 'profile')
        request.session['next'] = next_url
        form = LoginForms()

    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def profile_view(request):
    if request.role not in ['Admin', 'User']:
        return redirect('login')

    orders = request.user.get_orders()
    total_products_bought = sum(cart_item.quantity for order in orders for cart_item in order.cart.items.all())

    completed_orders = orders.filter(status='completed')[:5]
    pending_orders = orders.filter(status='processing')[:5]
    total_orders = orders.count()

    return render(request, 'profile.html', {
        'total_orders': total_orders,
        'total_products_bought': total_products_bought,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders
    })

@login_required(login_url='login')
def profile_update(request):
    if request.role not in ['Admin', 'User']:
        return redirect('login')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            success_message = "Your information has been updated successfully!"
            return render(request, 'profile_update.html', {'success_message': success_message})
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
