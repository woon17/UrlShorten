from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
        'username','email'
        ]
