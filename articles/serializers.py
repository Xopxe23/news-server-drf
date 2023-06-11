from rest_framework import serializers

from articles.models import Article, UserArticleRelation


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    likes = serializers.IntegerField(read_only=True)
    # comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author', 'category',
                  'created_at', 'is_published', 'likes')
        # , 'comments')

    # def get_comments(self, instance):
    #     relations = UserArticleRelation.objects.filter(article=instance)
    #     comments = []
    #     for relation in relations:
    #         comments.append({
    #             "user": relation.user.username,
    #             "comment": relation.comment
    #         })
    #     return comments


class UserArticleRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserArticleRelation
        fields = ('article', 'like', 'comment')
