from rest_framework.viewsets import ModelViewSet

from articles.models import Article
from articles.permissions import IsAuthorOrReadOnly
from articles.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().select_related('author')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()
