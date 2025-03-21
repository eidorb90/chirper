"""
Marcus Sweet
Brodie Rogers
<brodie.rogers@cune.students.edu>

forms.py
Last Edited : 3/20/25

Description:
    This module contains form definitions for the web application. 
    These forms are used to handle user input and validate data before processing.

Help:
    To use these forms, import the desired form class from this module and instantiate it in your view. 
    You can then render the form in your template and handle form submissions.

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    CustomUserCreationForm is a form for creating a new user with additional fields for first name, last name, and email.

    Fields:
        first_name (CharField): Required field for the user's first name.
        last_name (CharField): Required field for the user's last name.
        username (CharField): Required field for the user's username.
        email (EmailField): Required field for the user's email address.
        password1 (CharField): Required field for the user's password.
        password2 (CharField): Required field for confirming the user's password.

    Meta:
        model (User): The model associated with this form.
        fields (tuple): The fields to include in the form.

    Methods:
        save(commit=True):
            Saves the user instance with the provided data. If commit is True, the user is saved to the database.
            Returns the user instance.
    """
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


class chirpsForm(forms.Form):
    chirp = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'What\'s happening?'
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
        })
    )
    video = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
        })
    )

class replyForm(forms.Form):
    reply = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
            'placeholder': 'Reply'
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
        })
    )
    video = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'bg-gray-700 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 text-white',
            'style': 'height: 2.5rem; font-size: 90%; background-color: #374151; border-color: #4b5563; color: #FFFFFF;',
        })
    )