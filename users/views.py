from django.shortcuts import render, redirect
from .forms import RegisterForms, LoginForms, ProfileUpdateForm
from django.contrib.auth import authenticate as default_authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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
                return redirect('profile')

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
            
            # Authenticate with username or email
            user = authenticate(username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to profile page after successful login
            else:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForms()
    
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def profile_update(request):
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
