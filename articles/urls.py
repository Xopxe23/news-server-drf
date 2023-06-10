from rest_framework import routers

from articles.views import ArticleViewSet

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)

urlpatterns = router.urls
