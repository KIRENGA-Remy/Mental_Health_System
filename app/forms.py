from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Enter your first name")
    last_name = forms.CharField(max_length=30, required=True, help_text="Enter your last name")
    email = forms.EmailField(required=True, help_text="Enter your email")
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True) 

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'role']