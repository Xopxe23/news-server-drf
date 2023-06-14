import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Category, Article, UserArticleRelation


class ArticleSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='User1', is_staff=True)
        self.category1 = Category.objects.create(name="Test category 1")
        self.article1 = Article.objects.create(title="Test title 1", content="Test Content 1",
                                               author=self.user1, category=self.category1)

    def test_create_and_update(self):
        url = reverse('userarticlerelation-detail', args=(self.article1.id, ))
        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        self.client.patch(url, data=json_data, content_type='application/json')
        self.assertTrue(UserArticleRelation.objects.get(user=self.user1, article=self.article1).like)
        data = {
            "in_bookmarks": True
        }
        json_data = json.dumps(data)
        self.client.patch(url, json_data, content_type='application/json')
        self.assertTrue(UserArticleRelation.objects.get(user=self.user1, article=self.article1).in_bookmarks)
        self.assertEquals(UserArticleRelation.objects.all().count(), 1)
