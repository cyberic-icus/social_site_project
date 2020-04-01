from django import forms
from .models import Article

from tinymce import TinyMCE



class ArticleModelForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30, 'height':600}))
	class Meta:
		model = Article
		fields = [
			'header',
			'content'
			]
		
		
