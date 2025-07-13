from django.urls import path

from .views import CommentApiView

app_name = 'api'

urlpatterns = [
    path('comments/', CommentApiView.as_view(), name='comments'),
    path('comments/<int:id>/', CommentApiView.as_view(), name='comment'),
]