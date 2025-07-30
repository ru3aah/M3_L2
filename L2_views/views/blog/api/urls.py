from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (CommentViewSet, PostViewSet, SessionAuthApiView, \
    TokenAuthView, CategoryViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('posts', PostViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('session_auth/', SessionAuthApiView.as_view()),
    path('token_auth/', TokenAuthView.as_view()),
    path('jwt_token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt_token/refresh/', TokenRefreshView.as_view(),
            name='token_refresh'),
]