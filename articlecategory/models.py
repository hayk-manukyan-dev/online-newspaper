from django.db import models


class ArticleCategoryManager(models.Manager):
    def get_article_categories(self, request):
        return ArticleCategory.objects.all()



class ArticleCategory(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    description = models.CharField(max_length = 2000)

    objects = ArticleCategoryManager()

    def __str__(self):
        return self.name
