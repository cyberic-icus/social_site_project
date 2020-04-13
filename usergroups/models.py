from django.db import models
from tinymce import HTMLField
from django.urls import reverse

from project1.settings import AUTH_USER_MODEL
		
from django.contrib.auth.models import Group

class UserGroup(Group):
	created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
	photo = models.ImageField(upload_to='profile_pics/', default='default.jpg')
	slug = models.SlugField(max_length=40, unique=True)
	
	class Meta:
		ordering = ['-name']
	
	def get_absolute_url(self):
		return reverse('usergroups:usergroups-single', kwargs={'slug':self.slug})
		
	def __str__(self):
		return self.name
		
	
class UserGroupArticle(models.Model):
	author = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
	header = models.CharField(max_length = 25)
	content = HTMLField()
	pub_date = models.DateTimeField('Date Published', auto_now_add=True)
	
	class Meta:
		ordering = ['-pub_date']
	
	def __str__(self):
		return self.header
		
	def get_absolute_url(self):
		return reverse('articles:article-detail', kwargs={'id':self.id})
	

class UserGroupComment(models.Model):
	author = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
	post = models.ForeignKey(UserGroupArticle, on_delete=models.CASCADE)
	content = models.TextField(null=False)
	pub_date = models.DateTimeField('Date Published', auto_now_add=True)
	
	class Meta:
		ordering = ['pub_date']
		
	def get_absolute_url(self):
		return reverse('articles:comments-detail', kwargs={'id':self.post.id, 'pk':self.pk})
	
	def __str__(self):
		return f'{self.author.username}\'s Comment'