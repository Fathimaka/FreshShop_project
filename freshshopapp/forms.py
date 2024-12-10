from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2','first_name','last_name','email')
        help_texts = {
            'username': 'Use letters, numbers, and @/./+/-/_ only.',
            'password1': 'At least 8 characters, no common words.',
            'password2': 'Repeat the password for confirmation.',
            'first_name': 'Enter your first name.',
            'last_name': 'Enter your last name.',
            'email': 'Provide a valid email address.',
        }
        