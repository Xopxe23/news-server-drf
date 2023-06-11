from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор', related_name='articles')
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 verbose_name='Категория', related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    readers = models.ManyToManyField(User, through="UserArticleRelation",
                                     related_name='relationarticles')

    def __str__(self):
        return self.title[:50] + '...'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class UserArticleRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='relations')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='Статья',
                                related_name='relations')
    like = models.BooleanField(default=False, verbose_name='Лайк')
    comment = models.CharField(max_length=250, blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.user} - {self.article}'

    class Meta:
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'
