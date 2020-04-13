from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import render, get_object_or_404

from articles.models import Article
from users.models import CustomUser
from .models import UserGroup, UserGroupArticle, UserGroupComment
from .forms import UserGroupModelForm, ArticleModelForm, CommentModelForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from articles.forms import CommentModelForm as UserCommentModelForm

class UserGroupCreateView(CreateView):
	"""Регистрация юзера"""
	form_class = UserGroupModelForm
	template_name = 'usergroups/group_create.html'
	#success_url = '' # =================
	
	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)
	
	def get_success_url(self):
		slug_ = self.object.slug
		return reverse_lazy('usergroups:usergroups-single', kwargs={'slug':slug_})

class UserGroupPostView(LoginRequiredMixin, SingleObjectMixin, ListView, FormView):
	"""Показывает посты юзера и их автора"""
	template_name = 'usergroups/group_detail.html'
	context_object_name = 'grouparticle'
	form_class = ArticleModelForm
	
	# Тут должна быть функция, проверяющая вхождение юзера
	# в группу
	
	# Строго говоря, эти функции должны быть в модели
	def get_users(self):
		self.usergroup = get_object_or_404(UserGroup, slug=self.kwargs['slug'])
		return CustomUser.objects.filter(groups__id=self.usergroup.pk).count()
	
	def subscribe(self):
		self.usergroup = get_object_or_404(UserGroup, slug=self.kwargs['slug'])
		self.usergroup.user_set.add(self.request.user)
		return True
		
	def get(self, request, *args, **kwargs):
	    self.object = self.get_object()
	    return super().get(request, *args, **kwargs)
	
	def get_object(self):
		slug_ = self.kwargs.get('slug')
		return get_object_or_404(UserGroup, slug=slug_)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['author'] = self.object
		context['get_users'] = self.get_users()
		context['subscribe'] = self.subscribe()
		return context
		
	def get_queryset(self):
		return self.object.usergrouparticle_set.all()
		
	def get_success_url(self):
		slug_ = self.kwargs['slug']
		return reverse_lazy('usergroups:usergroups-single', kwargs={'slug':slug_})
	
	def form_valid(self, form):
		form.instance.author = get_object_or_404(UserGroup, slug=self.kwargs['slug'])
		if form.is_valid():
			form.save()
		return super().form_valid(form)
	
	
        
class UserGroupListView(LoginRequiredMixin, ListView):
	"""Показывает всех юзеров"""
	queryset = UserGroup.objects.all()
	template_name = 'usergroups/group_list.html'
	
class UserGroupUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	fields = ['name', 'photo', 'slug']
	template_name = 'users/update.html'
	
	def get_success_url(self):
		slug_ = self.object.slug
		return reverse_lazy('usergroups:usergroups-single', kwargs={'slug':slug_})
	
	def get_object(self):
		slug_ = self.kwargs.get('slug')
		return get_object_or_404(UserGroup, slug=slug_)
	
		
class UserGroupUsersListView(ListView):
	template_name = 'users/user_list.html'
	
	def get_queryset(self):
		self.usergroup = get_object_or_404(UserGroup, slug=self.kwargs['slug'])
		return CustomUser.objects.filter(groups__id=self.usergroup.pk)
		
# ============================================================================================
# ============================================================================================
# ============================================================================================

class UserGroupArticleListView(LoginRequiredMixin, ListView):
	template_name = 'usergroups/group_article_list.html'
	model = UserGroupArticle
	
	
class UserGroupArticleCreateView(LoginRequiredMixin, CreateView):
	"""Представление создания статьи."""
	template_name = 'usergroups/group_article_create.html'
	model = UserGroupArticle
	fields = ['header', 'content']
	
	
	def get_success_url(self):
		slug_ = self.kwargs['slug']
		return reverse_lazy('usergroups:usergroups-single', kwargs={'slug':slug_})
	
	def form_valid(self, form):
		form.instance.author = get_object_or_404(UserGroup, slug=self.kwargs['slug'])
		return super().form_valid(form)
	
	

class UserGroupArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	"""Представление изменения существующей статьи."""
	template_name = 'usergroups/group_article_create.html'
	form_class = ArticleModelForm
	
	def get_object(self):
		id_ = self.kwargs.get('id1')
		return get_object_or_404(UserGroupArticle, id=id_)
	
	def get_success_url(self):
		slug_ = self.kwargs['slug']
		return reverse_lazy('usergroups:usergroups-single', kwargs={'slug':slug_})
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author.created_by:
			return True
		return False



class UserGroupArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
	"""Представление удаления конкретной статьи."""
	template_name = 'usergroups/group_article_delete.html'
	
	def get_success_url(self):
		slug_ = self.kwargs.get('slug')
		return reverse_lazy('usergroups:usergroups-single', kwargs={'slug':slug_})
		
		
	def get_object(self):
		id_ = self.kwargs.get('id1')
		return get_object_or_404(UserGroupArticle, id=id_)
	
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author.created_by:
			return True
		return False
	
class UserGroupArticleDetailView(LoginRequiredMixin, SingleObjectMixin, ListView, FormView):
	"""Представление конкретной статьи."""
	template_name = 'usergroups/group_article_detail.html' 
	form_class = UserCommentModelForm
	
	def get_success_url(self):
		id_ = self.kwargs['id']
		slug_ = self.kwargs['slug']
		return reverse_lazy('usergroups:article-detail', kwargs={'id':id_, 'slug':slug_})
	
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(UserGroupArticle, id = id_)
	
	def get(self, request, *args, **kwargs):
	    self.object = self.get_object()
	    return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post'] = self.object
		return context
		
	def get_queryset(self):
		return self.object.usergroupcomment_set.all()
		
	def get_post(self):
		self.request.user_post = self.get_object()
		
	def form_valid(self, form):
		form.instance.post = self.get_object()
		form.instance.author = self.request.user
		return super().form_valid(form)

	
class UserGroupCommentListView(LoginRequiredMixin, ListView):
	"""Представление списка статей. НА УДАЛЕНИЕ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """
	template_name = 'comments/comment_list.html'
	model = UserGroupComment


class UserGroupCommentDetailView(LoginRequiredMixin, DetailView):
	"""Представление конкретной статьи."""
	template_name = 'usergroups/group_comment_detail.html'
	
	def get_object(self):
		pk_ = self.kwargs.get('pk')
		return get_object_or_404(UserGroupComment, pk=pk_)
	
	
class UserGroupCommentCreateView(LoginRequiredMixin, CreateView):
	"""Представление создания статьи."""
	template_name = 'comments/comment_create.html'
	model = UserGroupComment
	fields = ['content',]
	
	
	def get_success_url(self):
		id_ = self.kwargs.get('id')
		slug_ =self.kwargs.get('slug')
		return reverse_lazy('usergroups:article-detail', kwargs={'id':id_, 'slug':slug_})
		
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(UserGroupArticle, id = id_)
	
	def form_valid(self, form):
		form.instance.post = self.get_object()
		form.instance.author = get_object_or_404(UserGroup, slug=self.kwargs['slug'])
		return super().form_valid(form)
	
class UserGroupCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	"""Представление изменения существующей статьи."""
	template_name = 'comments/comment_create.html'
	model = UserGroupComment
	form_class = CommentModelForm
	
	def get_success_url(self):
		id_ = self.kwargs.get('id')
		slug_ =self.kwargs.get('slug')
		return reverse_lazy('usergroups:article-detail', kwargs={'id':id_, 'slug':slug_})
	
	def get_object(self):
		pk_ = self.kwargs.get('pk')
		return get_object_or_404(UserGroupComment, pk=pk_)
	
	def form_valid(self, form):
		form.instance.author = get_object_or_404(UserGroup, slug=self.kwargs['slug'])
		return super().form_valid(form)
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author.created_by:
			return True
		return False

class UserGroupCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
	"""Представление удаления конкретной статьи."""
	template_name = 'comments/comment_delete.html'
	model = UserGroupComment
	
	def get_success_url(self):
		id_ = self.kwargs.get('id')
		return reverse_lazy('articles:comments-list', kwargs={'id':id_})
		
		
	def get_object(self):
		pk_ = self.kwargs.get('pk')
		return get_object_or_404(UserGroupComment, pk = pk_)
	
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author.created_by:
			return True
		return False