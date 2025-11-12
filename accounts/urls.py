from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, IntegrationView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/integration/', IntegrationView.as_view(), name='integration'),
]
