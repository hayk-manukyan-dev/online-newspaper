from django.contrib import admin

from articlecategory.models import ArticleCategory

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']


admin.site.register(ArticleCategory, ArticleCategoryAdmin)