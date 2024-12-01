from django.shortcuts import render
from django.views import View

class RegisterView(View):
    def get(self, request):
        return render(request, 'register_page.html')
    
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')
