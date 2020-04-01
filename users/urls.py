from django.urls import path
from .views import UserRegisterView, UserPostView, UserListView, UserUpdateView
from django.contrib.auth import views 
from evileg_core.decorators import recaptcha

app_name = 'users'
urlpatterns = [
	path('', UserListView.as_view(), name='users-list'),
    path('register/', recaptcha(UserRegisterView.as_view()), name='users-register'),
    path('login/', views.LoginView.as_view(template_name='users/login.html'), name="users-login"),
    path('logout/', views.LogoutView.as_view(template_name='users/logout.html'), name="users-logout"),
    path('<username>/', UserPostView.as_view(), name='users-single'),
    path('<username>/update', UserUpdateView.as_view(), name='users-update'),
    
]