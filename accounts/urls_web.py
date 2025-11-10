from django.urls import path
from . import views_web

urlpatterns = [
    path('', views_web.home_view, name='home'),
    path('register/', views_web.register_view, name='register'),
    path('login/', views_web.login_view, name='login'),
    path('logout/', views_web.logout_view, name='logout'),
    path('profile/integration/', views_web.integration_view, name='integration'),
]
