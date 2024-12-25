from django.shortcuts import redirect
from django.http import HttpResponse

class RoleRequiredMiddleware:
    """
    Middleware để phân quyền: Admin, User, Guest
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_superadmin or request.user.is_admin:
                request.role = 'Admin'
            else:
                request.role = 'User'
        else:
            request.role = 'Guest'

        response = self.get_response(request)
        return response

