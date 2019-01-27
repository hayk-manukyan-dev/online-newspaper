from django.contrib import admin
from initialarticle.models import InitialArticle

class InitialArticleAdmin(admin.ModelAdmin):
    list_display = ['by', 'category', 'keywords', 'pk']

admin.site.register(InitialArticle, InitialArticleAdmin)