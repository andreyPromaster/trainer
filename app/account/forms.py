from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForms (UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ["username", "email", "password1","password2"]

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
		#email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
        fields = ["username",'email']

class ProfileUpdateForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'birth_date']