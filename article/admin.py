from django.contrib import admin

from article.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['initial', 'title', 'pk']


admin.site.register(Article, ArticleAdmin)


