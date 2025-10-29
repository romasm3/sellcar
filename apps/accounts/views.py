from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from apps.listings.models import Listing


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect("listings:home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Sėkmingai užsiregistravote!")
            return redirect("listings:home")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect("listings:home")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Sveiki sugrįžę, {username}!")
                return redirect("listings:home")
    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, "Sėkmingai atsijungėte.")
    return redirect("listings:home")


@login_required
def profile_view(request):
    """User profile view"""
    user_listings = Listing.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "user_listings": user_listings,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit_view(request):
    """Edit user profile"""
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilis sėkmingai atnaujintas!")
            return redirect("accounts:profile")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})
