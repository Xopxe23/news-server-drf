import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from articles.models import Category, Article
from articles.serializers import ArticleSerializer


class ArticleSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username='User1', is_staff=True)
        self.user2 = User.objects.create(username='User2', is_staff=True)
        self.category1 = Category.objects.create(name="Test category 1")
        self.category2 = Category.objects.create(name="Test category 2")
        self.article1 = Article.objects.create(title="Test title 1", content="Test Content 1",
                                               author=self.user1, category=self.category1)
        self.article2 = Article.objects.create(title="Test title 2", content="Test Content 2",
                                               author=self.user2, category=self.category2)
        self.article3 = Article.objects.create(title="Test title 3", content="Test Content 1",
                                               author=self.user2, category=self.category1)

    def test_get(self):
        url = reverse('article-list')
        response = self.client.get(url)
        articles = Article.objects.filter(is_published=True).annotate(
            likes=Count(Case(When(relations__like=True, then=1)))
        ).order_by('-created_at')
        serializer_data = ArticleSerializer(articles, many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('article-list')
        articles = Article.objects.filter(
            id__in=[self.article1.id, self.article3.id]
        ).annotate(likes=Count(Case(When(relations__like=True, then=1)))).order_by('-created_at')
        response = self.client.get(url, data={"search": "Test Content 1"})
        serializer_data = ArticleSerializer(articles, many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('article-list')
        articles = Article.objects.filter(is_published=True).annotate(
            likes=Count(Case(When(relations__like=True, then=1)))
        ).order_by('title')
        response = self.client.get(url, data={"ordering": "title"})
        serializer_data = ArticleSerializer(articles, many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer_data, response.data)

    def test_create_article(self):
        url = reverse('article-list')
        data = {
            "title": "Test title 1",
            "content": "Test Content 1",
            "author": self.user1.id,
            "category": self.category1.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(url, json_data, content_type="application/json")
        self.assertEquals(Article.objects.last().author, self.user1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Article.objects.all().count(), 4)

    def test_update_article(self):
        url = reverse('article-detail', args=(self.article1.id, ))
        data = {
            "title": self.article1.title,
            "content": "Test Content 1 updated",
            "author": self.user1.id,
            "category": self.category1.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, json_data, content_type="application/json")
        self.article1.refresh_from_db()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(self.article1.content, "Test Content 1 updated")

    def test_update_article_not_author(self):
        url = reverse('article-detail', args=(self.article1.id,))
        data = {
            "title": self.article1.title,
            "content": "Test Content 1 updated",
            "author": self.user1.id,
            "category": self.category1.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, json_data, content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.article1.refresh_from_db()
        self.assertEquals(self.article1.content, 'Test Content 1')

    def test_delete_article(self):
        url = reverse('article-detail', args=(self.article1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(self.user1)
        response = self.client.delete(url, content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
