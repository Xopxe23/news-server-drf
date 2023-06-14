from django.urls import path
from rest_framework import routers

from articles.views import (ArticleViewSet, CommentDeleteView,
                            CommentListCreateView, UserArticleRelationView,
                            UserViewSet)

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'articlerelation', UserArticleRelationView)
router.register(r'users', UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('articles/<int:article_id>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/delete', CommentDeleteView.as_view(), name='comment-delete'),
]
