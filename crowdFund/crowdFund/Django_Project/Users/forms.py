from django import forms
from django.db import models
from django.contrib.auth import authenticate,get_user_model
from .models import *
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"USERNAME"}))
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={"placeholder":"EMAIL ADDRESS"}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={"placeholder":"PASSWORD"}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={"placeholder":"CONFIRM PASSWORD"}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserProfile(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"phone"}),max_length=12,validators = [ RegexValidator(regex='^01[0|1|2|5][0-9]{8}$',message='Phone must be start 010, 011, 012, 015 and all number contains 11 digits',code='invalid number') ])
    image = forms.ImageField(label="")
    class Meta:
        model = Profile
        fields = ['phone','image']



class userLogin(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Enter username"}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={"placeholder":"Password"}))


