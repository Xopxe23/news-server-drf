from rest_framework import serializers

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author',
                  'category', 'created_at', 'is_published')
