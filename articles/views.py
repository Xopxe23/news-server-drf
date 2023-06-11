from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from articles.models import Article, UserArticleRelation
from articles.permissions import IsAuthorOrReadOnly
from articles.serializers import ArticleSerializer, UserArticleRelationSerializer, UserSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.filter(is_published=True).select_related('author').annotate(
        likes=Count(Case(When(relations__like=True, then=1)))
    )
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    # filterset_fields = ['category', 'author']
    ordering_fields = ['category', 'author', 'created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class UserArticleRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserArticleRelation.objects.all()
    serializer_class = UserArticleRelationSerializer
    lookup_field = 'article'

    def get_object(self):
        obj, _ = UserArticleRelation.objects.get_or_create(user=self.request.user,
                                                           article_id=self.kwargs['article'])
        return obj


class UserViewSet(mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
