from rest_framework import status
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ViewSet, ModelViewSet

from blog.models import Comment, Post
from blog.api.serializers import CommentSerializer, PostSerializer, PostListSerializer
from django.contrib.auth import authenticate, login
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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


class CommentApiView(ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    

class PostApiView(ModelViewSet):
    model = Post
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


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