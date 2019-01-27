from django.test import TestCase

import factory


from article.models import Article
from initialarticle.models import InitialArticle
from articlecategory.models import ArticleCategory

from django.contrib.auth import get_user_model
import datetime


class ArticleModelTest(Article):
    def setUpTestData(self):
        pass