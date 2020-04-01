from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	photo = models.ImageField(upload_to = 'profile_pics/', default = 'default.jpg')
	
	def __str__(self):
		return self.username
	
	def get_absolute_url(self):
		return reverse('users:users-single', kwargs={'username':self.username})