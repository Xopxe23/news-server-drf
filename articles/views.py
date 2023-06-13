from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from articles.models import Article, UserArticleRelation, Comment
from articles.permissions import IsAuthorOrReadOnly, IsAuthorOrOwner
from articles.serializers import ArticleSerializer, UserArticleRelationSerializer, UserSerializer, CommentSerializer


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
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all().prefetch_related('articles')
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(article=self.kwargs['article_id'])

    def perform_create(self, serializer):
        # serializer.validated_data['user'] = self.request.user
        # serializer.validated_data['article'] = Article.objects.get(pk=self.kwargs['article_id'])
        serializer.save(user=self.request.user,
                        article=Article.objects.get(pk=self.kwargs['article_id']))


class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthorOrOwner]

