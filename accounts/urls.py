from django.urls import path
from .views import RegisterView, LoginView, MeView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='api-register'),
    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('users/me/', MeView.as_view(), name='api-me'),
]
