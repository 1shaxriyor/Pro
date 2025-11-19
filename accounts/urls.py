from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    integration_view
)


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/integration/", integration_view, name="integration"),
]
