from django.contrib.auth.models import User
from django.db import models

from articles.tasks import sent_comment


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
        return f'{self.title[:30]}...'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    text = models.TextField(max_length=350, verbose_name='Текст')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Пользователь')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments', verbose_name='Статья')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Отправлено')

    def __str__(self):
        return f'{self.user} - {self.text[:30]}...'

    def save(self, *args, save_model=True, **kwargs):
        super().save(*args, **kwargs)
        if save_model:
            sent_comment.delay(self.id)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


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
    in_bookmarks = models.BooleanField(default=False, verbose_name='В закладки')

    def __str__(self):
        return f'{self.user} - {self.article}'

    class Meta:
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'
