from rest_framework import routers

from articles.views import ArticleViewSet, UserArticleRelationView, UserViewSet

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'articlerelation', UserArticleRelationView)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
