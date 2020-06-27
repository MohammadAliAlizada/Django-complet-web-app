from django.forms import ModelForm
#import pakege of register,login and authentication 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#//////////

#import models
from .models import *
class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class orderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'
	


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']