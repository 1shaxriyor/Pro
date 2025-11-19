from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from .forms import UserRegisterForm, ProfileForm


# ---------------------------
# Register view
# ---------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


# ---------------------------
# Login view
# ---------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri!")

    return render(request, "accounts/login.html")


# ---------------------------
# Logout
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect("home")


# ---------------------------
# Profile view
# ---------------------------
@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilingiz yangilandi!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


# ---------------------------
# Telegram integratsiya view
# ---------------------------
@login_required
def integration_view(request):
    context = {
        "bot_username": getattr(settings, "TELEGRAM_BOT_USERNAME", "MyBot"),
    }
    return render(request, "accounts/integration.html", context)
