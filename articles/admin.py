from django.contrib import admin

from articles.models import Article, Category, UserArticleRelation


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'is_published')
    list_display_links = ('id', 'author')
    search_fields = ('title', 'content')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(UserArticleRelation)
class UserArticleRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'article')
    list_display_links = ('id', 'user')
    list_filter = ('user',)
