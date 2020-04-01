from django.db import models
from tinymce import HTMLField
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	header = models.CharField(max_length = 25)
	content = HTMLField()
	pub_date = models.DateTimeField('Date Published', auto_now_add=True)
	
	class Meta:
		ordering = ['-pub_date']
	
	def __str__(self):
		return self.header
		
	def get_absolute_url(self):
		return reverse('articles:article-detail', kwargs={'id':self.id})
	

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Article, on_delete=models.CASCADE)
	content = models.TextField(null=False)
	pub_date = models.DateTimeField('Date Published', auto_now_add=True)
	
	class Meta:
		ordering = ['pub_date']
	
	def get_absolute_url(self):
		return reverse('articles:comments-detail', kwargs={'id':self.post.id, 'pk':self.pk})
	
	def __str__(self):
		return f'{self.author.username}\'s Comment'