"""

Marcus please do this file sinnce you were the one to make it

Brodie Rogers
admin.py
<brodie.rogers@cune.students.edu>

Description:
    aslkdfja;lskdjfaklsdvlkasjdvkasdlv
    aslkdjvalksdv;laj

Help:
    asdkfja;lsdjalskdjvklasdva
    sdvj;asdjvklasjdkvljaskdv
    asdvjajsdlva;sdklv

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-800 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Last Name'
        })
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Confirm Password'
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
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Password'
        })
    )