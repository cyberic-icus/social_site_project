from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import render, get_object_or_404

from articles.models import Article

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy

from articles.forms import ArticleModelForm


from django.views.generic import FormView
"""
1. Дополнить документацию представлений.
2. Сделать нормальное наследование.

"""


class UserRegisterView(CreateView):
	"""Регистрация юзера"""
	form_class = CustomUserCreationForm
	template_name = 'users/register.html'
	success_url = 'users/login/'
	
	def form_valid(self, form):
		if self.request.recaptcha_is_valid:
			form.save()
			return super().form_valid(form)
			
	


class UserPostView(LoginRequiredMixin, SingleObjectMixin, ListView, FormView):
	"""Показывает посты юзера и их автора"""
	template_name = 'users/profile.html'
	paginate_by = 5
	form_class = ArticleModelForm
	
	def get(self, request, *args, **kwargs):
	    self.object = self.get_object()
	    return super().get(request, *args, **kwargs)
	
	def get_object(self):
		username_ = self.kwargs.get('username')
		return get_object_or_404(CustomUser, username=username_)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['author'] = self.object
		return context
		
	def get_queryset(self):
		return self.object.article_set.all()
		
	def form_valid(self, form):
		form.instance.author = self.request.user
		form.save()
		return super().form_valid(form)
	
	def get_success_url(self):
		username_ = self.request.user.username
		return reverse_lazy('users:users-single', kwargs={'username':username_})
        
class UserListView(LoginRequiredMixin, ListView):
	"""Показывает всех юзеров"""
	queryset = CustomUser.objects.all()
	template_name = 'users/user_list.html'
	
class UserUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	fields = ['email', 'first_name', 'last_name', 'photo']
	template_name = 'users/update.html'
	
	def get_success_url(self):
		username_ = self.request.user.username
		return reverse_lazy('users:users-single', kwargs={'username':username_})
	
	def get_object(self):
		username_ = self.kwargs.get('username')
		return get_object_or_404(CustomUser, username=username_)
	
	def test_func(self):
		post = self.get_object()
		if self.request.user.username == self.kwargs.get('username'):
			return True
		return False

def about(request):
	me = CustomUser.objects.get(username='mike')
	context = {
		'user':me,
	}
	return render(request, 'about.html', context)