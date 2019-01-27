from django.test import TestCase

import factory


from article.models import Article
from initialarticle.models import InitialArticle
from articlecategory.models import ArticleCategory

from django.contrib.auth import get_user_model
import datetime


class ArticleModelFactory(factory.Factory):
    class Meta:
        model = Article

    initial = InitialArticle.objects.create(by = get_user_model().objects.first(), category = ArticleCategory.objects.first(), keywords = 'some_keywords')
    article = Article.objects.create(initial = initial, language = 'en', title = 'some title', description = 'some description', text = '<h1>some HTML text<h1>', main_image = 'web/logo.jpg', date_time = datetime.datetime(2018, 12, 31, 00, 5))

class ArticleModelTest(Article):
    def setUpTestData(self):
        pass