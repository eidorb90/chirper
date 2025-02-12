from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    # username = forms.EmailField(label='Email')

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm"}
        ),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm"}
        ),
        label="Password",
    )
    