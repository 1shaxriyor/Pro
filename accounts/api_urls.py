from django.urls import path
from .api_views import RegisterAPIView, UserMeAPIView, BotWebhookView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', UserMeAPIView.as_view(), name='api_user_me'),
    path('bot/webhook/', BotWebhookView.as_view(), name='bot_webhook'),
]
