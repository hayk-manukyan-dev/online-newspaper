from django.db import models
from django.contrib.auth import get_user_model
from articlecategory.models import ArticleCategory
from online_newspaper.settings import LANGUAGES, languages_dict

import copy

from processing.base.managers import Collect


class InitialArticleManager(models.Manager):

    def create_initial_article(self, by, category, keywords):
        try:
            article = InitialArticle(by = by, category = category, keywords = keywords)
            article.save()
            return article
        except:
            return False


    def edit_initial_article(self, article_keywords_object, by, category, keywords):
        article_keywords_object.by = by
        article_keywords_object.category = category
        article_keywords_object.keywords = keywords
        article_keywords_object.save()
        return article_keywords_object


    def get_by_keywords(self, keywords):
        return InitialArticle.objects.get(keywords = keywords)


    def initial_article_owner_is_requester(self, request, initial_article_object):
        if initial_article_object.by == request.user:
            return True
        return False




class InitialArticle(models.Model):
    by = models.ForeignKey(get_user_model(), null=True, on_delete = models.SET_NULL)
    category = models.ForeignKey(ArticleCategory, null=True, on_delete=models.CASCADE)
    keywords = models.CharField(max_length = 110, unique = True)

    objects = InitialArticleManager()

    def __str__(self):
        return self.keywords

