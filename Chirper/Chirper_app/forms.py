from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
        'class': 'border-2 border-gray-300 rounded-md p-2 w-full h-12',
        'style': 'width: 2.5rem; font-size: 1rem;'
    })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
        'class': 'border-2 border-gray-300 rounded-md p-2 w-full h-12',
        'style': 'width: 2.5rem; font-size: 1rem;'
    })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
        'class': 'border-2 border-gray-300 rounded-md p-2 w-full h-12',
        'style': 'width: 2.5rem; font-size: 1rem;'
    })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
        'class': 'border-2 border-gray-300 rounded-md p-2 w-full h-12',
        'style': 'width: 2.5rem; font-size: 1rem;'
    })
    )
    password2 = forms.CharField(
    widget=forms.PasswordInput(attrs={
        'class': 'border-2 border-gray-300 rounded-md p-2 w-full h-12',
        'style': 'width: 2.5rem; font-size: 1rem;'
    })
    )


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    # username = forms.EmailField(label='Email')

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'border-2 border-gray-300 rounded-md p-2 w-full h-12'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'border-2 border-gray-300 rounded-md p-2 w-full h-12'}),
        label='Password'
    )
    