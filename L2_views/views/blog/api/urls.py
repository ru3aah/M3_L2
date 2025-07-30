from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CommentViewSet, PostViewSet, SessionAuthApiView, \
    TokenAuthView, CategoryViewSet, CommentDetailAPIView, CommentListAPIView

app_name = 'api'

router = DefaultRouter()
#router.register('comments', CommentViewSet)
router.register('posts', PostViewSet)cd
router.register('categories', CategoryViewSet)

urlpatterns = [
    #path('comments/', CommentApiView.as_view(), name='comments'),
    #path('comments/<int:id>/', CommentApiView.as_view(), name='comment'),
    path('comments/', CommentListAPIView.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(),
         name='comment'),
    path('', include(router.urls)),
    path('session_auth/', SessionAuthApiView.as_view()),
    path('token_auth/', TokenAuthView.as_view()),

    path('jwt_token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt_token/refresh/', TokenRefreshView.as_view(),
            name='token_refresh'),
]