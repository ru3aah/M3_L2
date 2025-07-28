from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from ..models import Comment, Category, Tag, Post


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')
        read_only_fields = ('id',)

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Title is too short')
        return value


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class CommentSerializer(ModelSerializer):
    author = AuthorSerializer()
    #post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('content', 'created_at', 'updated_at', 'author')
        read_only_fields = ('created_at', 'updated_at', 'author')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'category', 'tags',
                  'comments', 'created_at', 'updated_at', 'status')
        read_only_fields = ('id', 'comments', 'created_at', 'updated_at',
                            'category', 'tags')


class PostListSerializer(ModelSerializer):
    #author = PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),
                                  #  read_only=True)
    class Meta:
        model = Post
        queryset = Post.objects.all()
        fields = ('id', 'author', 'title', 'status')


