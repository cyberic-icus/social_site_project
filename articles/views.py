from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView,DetailView,ListView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from .models import Article, Comment
from .forms import ArticleModelForm, CommentModelForm
from django.views.generic import FormView

"""
1. Дополнить документацию представлений.
2. Сделать нормальное наследование.

"""




class ArticleListView(LoginRequiredMixin, ListView):
	"""Представление списка статей. НА УДАЛЕНИЕ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """
	template_name = 'articles/article_list.html'
	queryset = Article.objects.all()
	
	
class ArticleDetailView(LoginRequiredMixin, SingleObjectMixin, ListView, FormView):
	"""Представление конкретной статьи."""
	template_name = 'articles/article_detail.html'
	form_class = CommentModelForm
	
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article, id = id_)
	
	def get(self, request, *args, **kwargs):
	    self.object = self.get_object()
	    return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post'] = self.object
		return context
		
	def get_queryset(self):
		return self.object.comment_set.all()
		
	def get_post(self):
		self.request.user_post = self.get_object()
		
	def form_valid(self, form):
		form.instance.post = self.get_object()
		form.instance.author = self.request.user
		if form.is_valid():
			form.save()
		return super().form_valid(form)
		
	
	def get_success_url(self):
		id_ = self.kwargs.get('id')
		return reverse_lazy('articles:article-detail', kwargs={'id':id_})


	
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
	form_class = ArticleModelForm
	
	def get_object(self):
		id_ = self.kwargs.get('id1')
		return get_object_or_404(Article, id=id_)
	
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
	"""Представление удаления конкретной статьи."""
	template_name = 'articles/article_delete.html'
	
	def get_success_url(self):
		username_ = self.request.user.username
		return reverse_lazy('users:users-single', kwargs={'username':username_})
		
		
	def get_object(self):
		id_ = self.kwargs.get('id1')
		return get_object_or_404(Article, id=id_)
	
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
	return render(request, 'about.html', {})
	
def home(request):
	return render(request, 'home.html', {})

	
class CommentListView(LoginRequiredMixin, ListView):
	"""Представление списка статей. НА УДАЛЕНИЕ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """
	template_name = 'comments/comment_list.html'
	model = Comment


class CommentDetailView(LoginRequiredMixin, DetailView):
	"""Представление конкретной статьи."""
	template_name = 'comments/comment_detail.html'
	
	def get_object(self):
		pk_ = self.kwargs.get('pk')
		return get_object_or_404(Comment, pk = pk_)
	
	
class CommentCreateView(LoginRequiredMixin, CreateView):
	"""Представление создания статьи."""
	template_name = 'comments/comment_create.html'
	model = Comment
	fields = ['content',]
	
	
	def get_success_url(self):
		id_ = self.kwargs.get('id')
		return reverse_lazy('articles:article-detail', kwargs={'id':id_})
		
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article, id = id_)
	
	def form_valid(self, form):
		form.instance.post = self.get_object()
		form.instance.author = self.request.user
		return super().form_valid(form)
	
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	"""Представление изменения существующей статьи."""
	template_name = 'comments/comment_create.html'
	model = Comment
	form_class = CommentModelForm
	
	
	def get_object(self):
		pk_ = self.kwargs.get('pk')
		return get_object_or_404(Comment, pk = pk_)
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
	"""Представление удаления конкретной статьи."""
	template_name = 'comments/comment_delete.html'
	model = Comment
	
	def get_success_url(self):
		id_ = self.kwargs.get('id')
		return reverse_lazy('articles:article-detail', kwargs={'id':id_})
		
		
	def get_object(self):
		pk_ = self.kwargs.get('pk')
		return get_object_or_404(Comment, pk = pk_)
	
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False