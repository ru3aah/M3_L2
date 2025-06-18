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
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(),
         name='post_delete'),
    path('posts/<int:post_id>/comment/', views.create_comment,
         name='comment_create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(),
         name='author_detail')
]