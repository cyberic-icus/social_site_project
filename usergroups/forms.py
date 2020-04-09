from django import forms
from .models import UserGroup, UserGroupArticle, UserGroupComment

from tinymce import TinyMCE

class UserGroupModelForm(forms.ModelForm):
	class Meta:
		model = UserGroup
		fields = [
			'name',
			'slug',
			'photo',
		]

class ArticleModelForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30, 'height':600}))
	class Meta:
		model = UserGroupArticle
		fields = [
			'header',
			'content'
			]
		
		
class CommentModelForm(forms.ModelForm):
	class Meta:
		model = UserGroupComment
		fields = [
			'content'
			]