from django.db import models

from configuration.transfers import readJson

models_config = readJson('configuration/json/models.json')

class ArticleCategoryManager(models.Manager):
    def get_article_categories(self, request):
        return ArticleCategory.objects.all()



class ArticleCategory(models.Model):
    name = models.CharField(max_length = models_config["ArticleCategory"]["name"]["max_length"], unique = True)
    description = models.CharField(max_length = models_config["ArticleCategory"]["description"]["max_length"])

    objects = ArticleCategoryManager()

    def __str__(self):
        return self.name
