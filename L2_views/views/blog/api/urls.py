from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentApiView, PostApiView, SessionAuthApiView, \
    TokenAuthView

app_name = 'api'

router = DefaultRouter()
router.register('comments', CommentApiView)
router.register('posts', PostApiView)

urlpatterns = [
    #path('comments/', CommentApiView.as_view(), name='comments'),
    #path('comments/<int:id>/', CommentApiView.as_view(), name='comment'),
    path('', include(router.urls)),
    path('session_auth/', SessionAuthApiView.as_view()),
    path('token_auth/', TokenAuthView.as_view()),
]