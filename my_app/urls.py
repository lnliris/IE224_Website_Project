from django.urls import path
from .views import RegisterView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'), 
]