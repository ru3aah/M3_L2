from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Comment, Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Title is too short')
        return value

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    #post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('content', 'created_at', 'updated_at', 'author')
        read_only_fields = ('created_at', 'updated_at', 'author')

class TagSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'category', 'tags', 'comments',
                  'created_at', 'updated_at', 'status')
        read_only_fields = ('id', 'comments', 'created_at', 'updated_at',
                            'category', 'tags')



