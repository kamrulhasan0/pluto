from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username',  max_length = 100)
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label = 'First Name', max_length = 200)
    last_name = forms.CharField(label = 'Last Name', max_length = 200)
    email = forms.EmailField(label = 'Email')
    class Meta:
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'email',
            'password1', 'password2'
        ]
