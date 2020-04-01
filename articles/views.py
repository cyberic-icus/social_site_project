from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView,DetailView,ListView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Article
from .forms import ArticleModelForm


"""
1. Дополнить документацию представлений.
2. Сделать нормальное наследование.

"""




class ArticleListView(LoginRequiredMixin, ListView):
	"""Представление списка статей. НА УДАЛЕНИЕ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """
	template_name = 'articles/article_list.html'
	queryset = Article.objects.all()
	
class ArticleDetailView(LoginRequiredMixin, DetailView):
	"""Представление конкретной статьи."""
	template_name = 'articles/article_detail.html'
	
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article, id = id_)
	
class ArticleCreateView(LoginRequiredMixin, CreateView):
	"""Представление создания статьи."""
	template_name = 'articles/article_create.html'
	model = Article
	fields = ['header', 'content']
	
	
	def get_success_url(self):
		username_ = self.request.user.username
		return reverse_lazy('users:users-single', kwargs={'username':username_})
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	"""Представление изменения существующей статьи."""
	template_name = 'articles/article_create.html'
	model = Article
	form_class = ArticleModelForm
	
	
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article, id = id_)
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
	"""Представление удаления конкретной статьи."""
	template_name = 'articles/article_delete.html'
	queryset = Article.objects.all()
	form_class = ArticleModelForm
	
	def get_success_url(self):
		username_ = self.request.user.username
		return reverse_lazy('users:users-single', kwargs={'username':username_})
		
		
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article, id = id_)
	
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
	return render(request, 'about.html', {})
	

	
	
	
