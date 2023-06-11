from rest_framework import routers

from articles.views import ArticleViewSet, UserArticleRelationView

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'articlerelation', UserArticleRelationView)

urlpatterns = router.urls
