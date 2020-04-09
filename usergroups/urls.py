from django.urls import path, include
from django.contrib.auth import views 

app_name = 'usergroups'








from .views import (
	UserGroupCreateView, 
	UserGroupPostView, 
	UserGroupListView, 
	UserGroupUpdateView, 
	UserGroupUsersListView,
	UserGroupArticleListView,			
	UserGroupArticleCreateView,
	UserGroupArticleUpdateView,
	UserGroupArticleDeleteView,
	UserGroupArticleDetailView,
	UserGroupCommentListView,
	UserGroupCommentDetailView,
	UserGroupCommentCreateView,
	UserGroupCommentUpdateView,
	UserGroupCommentDeleteView,
	
)



comment_urlpatterns = [
	path('', UserGroupArticleDetailView.as_view(), name='article-detail'),
	path('comments/', UserGroupCommentListView.as_view(), name='comments-list'),
	path('comments/<int:pk>/', UserGroupCommentDetailView.as_view(), name='comments-detail'),
	path('comments/create/', UserGroupCommentCreateView.as_view(), name='comments-create'),
	path('comments/<int:pk>/update/', UserGroupCommentUpdateView.as_view(), name='comments-update'),
	path('comments/<int:pk>/delete/', UserGroupCommentDeleteView.as_view(), name='comments-delete'),

]


article_urlpatterns = [
	path('', UserGroupArticleListView.as_view(), name='article-list'),
	path('<int:id>/', include(comment_urlpatterns)),
    
    
    path('create/', UserGroupArticleCreateView.as_view(), name='article-create'),
    path('<int:id1>/update/', UserGroupArticleUpdateView.as_view(), name='article-update'),
    path('<int:id1>/delete/', UserGroupArticleDeleteView.as_view(), name='article-delete'),
   
    
]







urlpatterns = [
	path('', UserGroupListView.as_view(), name='usergroups-list'),
    path('create/', UserGroupCreateView.as_view(), name='usergroups-create'),
    path('<slug>/', UserGroupPostView.as_view(), name='usergroups-single'),
    path('<slug>/update', UserGroupUpdateView.as_view(), name='usergroups-update'),
    path('<slug>/users', UserGroupUsersListView.as_view(), name='usergroups-users'),
    path('<slug>/articles/', include(article_urlpatterns)),
    
]