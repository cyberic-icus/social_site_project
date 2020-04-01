from django.contrib import admin
from .models import CustomUser


from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['email', 'username', 'first_name', 'last_name', 'photo' ]
	
admin.site.register(CustomUser, CustomUserAdmin)