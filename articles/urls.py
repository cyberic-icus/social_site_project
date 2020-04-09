from django.urls import path, include
from .views import (
	ArticleListView,			
	ArticleDetailView,
	ArticleCreateView,
	ArticleUpdateView,
	ArticleDeleteView,
	CommentListView,
	CommentDetailView,
	CommentCreateView,
	CommentUpdateView,
	CommentDeleteView,
	
)
app_name = 'articles'


comment_urlpatterns = [
	path('',ArticleDetailView.as_view(), name='article-detail'),
	path('comments/', CommentListView.as_view(), name='comments-list'),
	path('comments/<int:pk>/', CommentDetailView.as_view(), name='comments-detail'),
	path('comments/create/', CommentCreateView.as_view(), name='comments-create'),
	path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comments-update'),
	path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comments-delete'),

]


urlpatterns = [
	path('', ArticleListView.as_view(), name='article-list'),
	path('<int:id>/', include(comment_urlpatterns)),
    
    
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<int:id1>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<int:id1>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
   
    
]

"""
    path('', CommentListView.as_view(), name='comments-list'),
    path('<int:id>', CommentDetailView.as_view(), name='comments-detail'),
    path('create/', CommentCreateView.as_view(), name='comments-create'),
    path('update/', CommentUpdateView.as_view(), name='comments-update'),
    path('delete/', CommentDeleteView.as_view(), name='comments-delete'),"""