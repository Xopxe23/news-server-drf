from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from articles.models import Article
from articles.permissions import IsAuthorOrReadOnly
from articles.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.filter(is_published=True).select_related('author')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    # filterset_fields = ['category', 'author']
    ordering_fields = ['category', 'author', 'created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()
