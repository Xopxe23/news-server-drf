from django.contrib.auth.models import User
from rest_framework import serializers

from articles.models import Article, Comment, UserArticleRelation


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'article', 'user', 'text', 'created_at')
        read_only_fields = ('article', 'user')


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author', 'category',
                  'created_at', 'is_published', 'likes')


class UserArticleRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserArticleRelation
        fields = ('article', 'like', 'comment')


class UserSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', "username", "first_name", "last_name",
                  "articles")
