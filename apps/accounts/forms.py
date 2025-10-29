from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="El. paštas")
    phone = forms.CharField(max_length=20, required=False, label="Telefonas")
    city = forms.CharField(max_length=100, required=False, label="Miestas")

    class Meta:
        model = User
        fields = ("username", "email", "phone", "city", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Vartotojo vardas",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Slaptažodis", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="El. paštas")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "profile_image",
            "bio",
        )
        labels = {
            "username": "Vartotojo vardas",
            "first_name": "Vardas",
            "last_name": "Pavardė",
            "phone": "Telefonas",
            "city": "Miestas",
            "profile_image": "Profilio nuotrauka",
            "bio": "Apie mane",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"
