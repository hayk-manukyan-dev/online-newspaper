from django.shortcuts import HttpResponse, render
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator

from article.models import Article
from articlecategory.models import ArticleCategory

import json

from processing.base.managers import MessageManager, Collect

from configuration.transfers import readJson


class GetArticleByKeywords(TemplateView):
    template_name = 'article/get_article.html'

    def get(self, request, *args, **kwargs):
        self.article = Article.objects.get_article(kwargs['keywords'], language = kwargs['language'])
        return super(GetArticleByKeywords, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GetArticleByKeywords, self).get_context_data(**kwargs)
        context['article'] = self.article
        return context



class GetArticlesByCategory(TemplateView):
    template_name = 'article/category_articles.html'

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(initial__category__pk = kwargs['category_pk'], language = kwargs['language']).order_by('-date_time')
        articles_paginator = Paginator(articles, 20)
        self.articles_paginated =  articles_paginator.page(kwargs['page'])
        return super(GetArticlesByCategory, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GetArticlesByCategory, self).get_context_data(**kwargs)
        context['category_articles'] = self.articles_paginated
        return context


class GetMixedArticles(TemplateView):
    template_name = 'article/mixed_articles.html'

    def get(self, request, *args, **kwargs):
        mixed_articles = readJson('configuration/json/webconfig.json')['mixed_articles']
        self.collect_articles = []
        for mixed_article in mixed_articles:
            self.collect_articles.append(Article.objects.filter(initial__category__name = mixed_article, language = kwargs['language']).order_by('-date_time')[:mixed_articles[mixed_article]])
        all_actegories = [category.name for category in ArticleCategory.objects.all()]
        for category in all_actegories:
            if not category in mixed_articles:
                self.collect_articles.append(Article.objects.filter(initial__category__name = category, language = kwargs['language']).order_by('-date_time')[0:5])
        return super(GetMixedArticles, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GetMixedArticles, self).get_context_data(**kwargs)
        context['mixed_articles'] = self.collect_articles
        return context


def getArticlePartHTML(request, *args, **kwargs):
    if request.method == 'GET':
        article = Article.objects.get_article(kwargs['keywords'], language = kwargs['language'])
        return render(request, 'article/article_card.html', {'article' : article})
    return HttpResponse(Collect(response = 'filure', message = str(MessageManager().getMessage('bad_request'))).get_json(), content_type = 'application/json')