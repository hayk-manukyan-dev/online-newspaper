from article.models import Article
from initialarticle.models import InitialArticle
from online_newspaper.settings import LANGUAGES, languages_dict
from processing.base.managers import Collect

import copy

from django import template


register = template.Library()


@register.filter(name='possible_languges')
def get_possible_languages(self):
    articles = Article.objects.filter(initial=self)
    existed_languages = copy.deepcopy(languages_dict)
    for article in articles:
        if Article.objects.language_exist(self.keywords, article.language):
            del existed_languages[article.language]
    collect_languages = []
    for LANGUAGE in LANGUAGES:
        if LANGUAGE[0] in existed_languages != True:
            collect_languages.append(Collect(code=LANGUAGE[0], label=LANGUAGE[1]).obj)
    return collect_languages


@register.filter(name='article_exist_languages')
def get_article_languages(self):
    articles = Article.objects.filter(initial__keywords = self.keywords)
    languages = []
    for article_filtred in articles:
        for LANGUAGE in LANGUAGES:
            if LANGUAGE[0] == article_filtred.language:
                languages.append({'code': LANGUAGE[0], 'label': LANGUAGE[1]})
    return languages


@register.filter(name='get_articles')
def get_articles_of_initialarticle(self):
    return Article.objects.filter(initial=self)