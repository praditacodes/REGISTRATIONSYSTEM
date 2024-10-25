from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Validation Rules
        if len(password) < 8:
            raise ValidationError("Your password must contain at least 8 characters.")
        if password.isdigit():
            raise ValidationError("Your password can't be entirely numeric.")
        if password.lower() in ['password', '12345678', 'qwerty']:  # Add more common passwords as needed
            raise ValidationError("Your password can't be a commonly used password.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password confirmation does not match.")

        return cleaned_data

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
