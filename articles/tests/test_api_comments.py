import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from articles.models import Category, Article, Comment
from articles.serializers import CommentSerializer


class CommentSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username='User1', is_staff=True)
        self.user2 = User.objects.create(username='User2', is_staff=True)
        self.category1 = Category.objects.create(name="Test category 1")
        self.article1 = Article.objects.create(title="Test title 1", content="Test Content 1",
                                               author=self.user1, category=self.category1)
        self.comment1 = Comment.objects.create(text="Test comment 1", article=self.article1, user=self.user1)
        self.comment2 = Comment.objects.create(text="Test comment 2", article=self.article1, user=self.user2)
        self.comment3 = Comment.objects.create(text="Test comment 3", article=self.article1, user=self.user2)

    def test_get(self):
        url = reverse('comment-list', args=(self.article1.id, ))
        self.client.force_login(self.user1)
        comments = Comment.objects.filter(article=self.article1.id)
        serializer_data = CommentSerializer(comments, many=True).data
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

    def test_post(self):
        url = reverse('comment-list', args=(self.article1.id, ))
        self.client.force_login(self.user1)
        data = {
            "text": "Test comment 3"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Comment.objects.last().text, "Test comment 3")
        self.assertEquals(Comment.objects.filter(article=self.article1.id).count(), 4)

    def test_delete(self):
        url = 'comment-delete'
        self.client.force_login(self.user2)
        response = self.client.delete(reverse(url, args=(self.comment1.id, )),
                                      content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(reverse(url, args=(self.comment2.id, )),
                                      content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.force_login(self.user1)
        response = self.client.delete(reverse(url, args=(self.comment3.id,)),
                                      content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Comment.objects.all().count(), 1)
