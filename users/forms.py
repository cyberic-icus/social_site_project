from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = (
			'username', 
			'email', 
			'first_name', 
			'last_name', 
			'photo')
		
class CustomUserChangeForm(UserChangeForm):
	password = None
	class Meta:
		model = User
		fields = ('photo',)
		