from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:id>/', views.PostDetailView.as_view(), name='post_details'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:id>/update/', views.PostUpdateView.as_view(),
         name='post_edit'),
    path('posts/<int:id>/delete/', views.PostDeleteView.as_view(),  # Fixed: changed from 'post/<int:pk>' to 'posts/<int:id>'
         name='post_delete'),
    path('posts/<int:post_id>/comment/', views.create_comment,
         name='comment_create'),
    path('comments/<int:id>/delete/', views.DeleteCommentView.as_view(),  # Added: missing comment delete URL
         name='comment_delete'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(),
         name='author_detail'),
    path('contacts/', views.contacts, name='contacts')
]