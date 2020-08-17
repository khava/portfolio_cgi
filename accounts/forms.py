from django import forms
from django.contrib.auth.forms import UserChangeForm as auth_UserChangeForm
from django.contrib.auth.forms import UserCreationForm as auth_UserCreationForm

from accounts.models import User


class SignupForm(auth_UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email')


class UserChangeForm(auth_UserChangeForm):
    class Meta(auth_UserChangeForm.Meta):
        model = User
        fields = ('username', 'email')


class UserCreationForm(auth_UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email')
