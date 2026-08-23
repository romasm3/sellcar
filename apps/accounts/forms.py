from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """Registracija su apsauga nuo botų (žr. apps/accounts/antispam.py).

    Honeypot `website` yra šablone (ne formos laukas), o čia tikrinam
    vienadienius pašto domenus — el. pašto patvirtinimo kol kas nėra,
    todėl tai vienintelis adreso tikrumo barjeras.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        from .antispam import domenas_vienadienis, ZINUTES
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Šis el. paštas jau užregistruotas.'))
        if domenas_vienadienis(email):
            raise forms.ValidationError(ZINUTES['disposable'])
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'phone_number',
            'phone_number_secondary',
            'street',
            'house_number',
            'city',
            'country',
            'profile_picture',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+370 600 00000'}),
            'phone_number_secondary': forms.TextInput(attrs={'placeholder': '+370 600 00000'}),
            'street': forms.TextInput(attrs={'placeholder': 'Street name'}),
            'house_number': forms.TextInput(attrs={'placeholder': 'House number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password'
        })
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )