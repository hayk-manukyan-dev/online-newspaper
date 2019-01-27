from article.models import Article
from initialarticle.models import InitialArticle
from online_newspaper.settings import LANGUAGES

from django import template


register = template.Library()


@register.filter(name='existed_languages')
def get_article_languages(self):
    initial_article = InitialArticle.objects.get(keywords = self.initial.keywords)
    articles = Article.objects.filter(initial__keywords=initial_article)
    languages = []
    for article_filtred in articles:
        if article_filtred.language != self.language:
            for LANGUAGE in LANGUAGES:
                if LANGUAGE[0] == article_filtred.language:
                    languages.append({'code': LANGUAGE[0], 'name': LANGUAGE[1]})
    return languages

