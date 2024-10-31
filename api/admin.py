from django.contrib import admin
from .models import *

@admin.register(Article)
class ArticleAmib(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'like_article_count')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    
@admin.register(LikeArticle)
class LikeArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'article__title')
    list_filter = ('created_at',)