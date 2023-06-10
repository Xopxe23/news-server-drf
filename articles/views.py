from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from articles.models import Article
from articles.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().select_related('author')
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()
