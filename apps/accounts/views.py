from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomPasswordChangeForm,
)
from .models import Profile


# ============================================
# HOME PAGE (temporary)
# ============================================


def home(request):
    """Temporary home page"""
    return render(request, "home.html")


# ============================================
# REGISTRATION & LOGIN/LOGOUT
# ============================================


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect("accounts:home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created! You can now login.")

            # Auto login after registration (optional)
            login(request, user)
            return redirect("accounts:home")
        else:
            messages.error(request, "Please fix the errors.")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect("accounts:home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")

                # Redirect to next page if specified
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect("accounts:home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect("accounts:home")


# ============================================
# PASSWORD RESET (via email)
# ============================================


class CustomPasswordResetView(PasswordResetView):
    """Password reset view - send email"""

    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")

    def form_valid(self, form):
        messages.success(
            self.request, "Password reset instructions sent to your email."
        )
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Password reset done view - confirmation that email sent"""

    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Password reset confirm view - new password"""

    form_class = CustomSetPasswordForm
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

    def form_valid(self, form):
        messages.success(
            self.request, "Password successfully changed! You can now login."
        )
        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Password reset complete view - completion"""

    template_name = "accounts/password_reset_complete.html"


# ============================================
# PASSWORD CHANGE (for logged in users)
# ============================================


@login_required
def password_change(request):
    """Password change for logged in users"""
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important: update session so user doesn't get logged out
            update_session_auth_hash(request, user)
            messages.success(request, "Password successfully changed!")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Please fix the errors.")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "accounts/password_change.html", {"form": form})


# ============================================
# USER PROFILE
# ============================================


@login_required
def profile(request):
    """User profile view"""
    from apps.listings.models import Listing
    
    # Get user listings
    active_listings = Listing.objects.filter(
        seller=request.user, status='active'
    ).select_related('brand', 'model').order_by('-created_at')[:6]
    
    sold_listings = Listing.objects.filter(
        seller=request.user, status='sold'
    ).select_related('brand', 'model').order_by('-created_at')[:6]
    
    active_count = Listing.objects.filter(seller=request.user, status='active').count()
    sold_count = Listing.objects.filter(seller=request.user, status='sold').count()

    context = {
        "user": request.user,
        "active_listings": active_listings,
        "sold_listings": sold_listings,
        "active_count": active_count,
        "sold_count": sold_count,
        "saved_count": 0,  # TODO: implement saved listings count
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit(request):
    """User profile edit"""
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile successfully updated!")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Please fix the errors.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "accounts/profile_edit.html", context)


# ============================================
# ACCOUNT SETTINGS
# ============================================


@login_required
def settings(request):
    """Account settings main page"""
    context = {
        "user": request.user,
    }
    return render(request, "accounts/settings.html", context)


@login_required
def update_notifications(request):
    """Update notification preferences"""
    if request.method == "POST":
        profile = request.user.profile

        # Get notification preferences from form
        profile.email_notifications = request.POST.get("email_notifications") == "on"
        profile.marketing_emails = request.POST.get("marketing_emails") == "on"
        profile.sms_notifications = request.POST.get("sms_notifications") == "on"

        profile.save()
        messages.success(request, "Notification settings updated successfully!")
        return redirect("accounts:settings")

    return render(request, "accounts/settings_notifications.html")


@login_required
def update_privacy(request):
    """Update privacy settings"""
    if request.method == "POST":
        profile = request.user.profile

        # Get privacy preferences from form
        profile.show_email = request.POST.get("show_email") == "on"
        profile.show_phone = request.POST.get("show_phone") == "on"
        profile.public_profile = request.POST.get("public_profile") == "on"

        profile.save()
        messages.success(request, "Privacy settings updated successfully!")
        return redirect("accounts:settings")

    return render(request, "accounts/settings_privacy.html")


@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user

        # Verify password before deletion
        if user.check_password(password):
            # Log out and delete user
            logout(request)
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect("accounts:home")
        else:
            messages.error(request, "Incorrect password. Account was not deleted.")
            return redirect("accounts:delete_account")

    return render(request, "accounts/delete_account.html")