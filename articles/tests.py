from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Article

class ArticleTests(TestCase):
    def test_create_article(self):
    	User = get_user_model()
    	user = User.objects.create_user(username='Steve', email='hkk@mail.ru')
    	article = Article.objects.create(author=user, header='Test Article', content='<h1>Testing...</h1>')
    	self.assertEqual(article.author.username, 'Steve')
    	self.assertEqual(article.header, 'Test Article')
    	self.assertEqual(article.content, '<h1>Testing...</h1>')
            
    
