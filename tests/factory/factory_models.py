from django.contrib.auth import get_user_model

import datetime
import factory

from user.models import User
from article.models import Article
from initialarticle.models import InitialArticle
from articlecategory.models import ArticleCategory


class UserModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'Nofname'
    last_name = 'Nolname'
    email = 'some@email.none'
    email_confirmed = True
    avatar = factory.LazyAttribute(factory.django.ImageField()._make_data({'width': 1024, 'height': 768}), 'example.jpg')

print(UserModelFactory())
'''
class InitialArticleModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = InitialArticle

    by = get_user_model().objects.first()
    category = ArticleCategory.objects.first()
    keywords = 'some_keywords'


class ArticleModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = Article

    initial = InitialArticleModelFactory()
    language = 'en'
    title = 'some title'
    description = 'some description'
    text = '<h1>some HTML text<h1>'
    main_image = 'web/logo.jpg'
    date_time = datetime.datetime(2018, 12, 31, 00, 5)
'''