from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, \
    IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import PostFilter
from .paginations import CommentPagination, PostListPagination
from .permissions import IsAuthorOrReadOnly, NoDeletePermission
from ..models import Category, Comment, Post
from .serializers import PostSerializer, CommentSerializer, CategorySerializer, PostListSerializer

# class CommentApiView(APIView):
#    def get(self, request, *args, **kwargs):
#        if 'id' in kwargs:
#            comments = Comment.objects.filter(post_id=kwargs['id'])
#        else:
#            comments = Comment.objects.all()
#        serializer = CommentSerializer(comments, many=not 'id' in kwargs)
#        return Response(serializer.data)
#
#    def post(self, request, *args, **kwargs):
#        serializer = CommentSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=400)


class CategoryViewSet(ModelViewSet):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [NoDeletePermission | IsAdminUser]


class CommentViewSet(ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CommentPagination
    

class PostViewSet(ModelViewSet):
    model = Post
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    pagination_class = PostListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'tags', 'author', 'content']
    search_fields = ['title', 'content','category__title', 'tags__title']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ('-created_at')


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SessionAuthApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'status': 'error',
                 'message': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {'status': 'error',
                     'message': 'Invalid credentials'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        #session id in cookie
        login(request, user)

        return Response({'status': 'success', 'message': 'User logged in'})


    def get(self, request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)

class TokenAuthView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'status': 'error',
                 'message': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {'status': 'error',
                     'message': 'Invalid credentials'},
                    status=status.HTTP_400_BAD_REQUEST
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status': 'success', 'message': 'User logged in',
                         'token': token.key})