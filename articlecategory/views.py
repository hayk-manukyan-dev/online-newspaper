from django.shortcuts import redirect, HttpResponse
from django.views.generic import TemplateView
from django.views import View
from processing.base.managers import MessageManager
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from articlecategory.models import ArticleCategory, ArticleCategoryManager
from articlecategory.forms import ArticleCategoryModelForm

from processing.base.decorators import group_required
from processing.base.managers import Collect

import json



class CreateArticleCategory(TemplateView):
    template_name = 'articlecategory/create_article_category.html'

    @method_decorator(login_required(login_url='/login'))
    @method_decorator(group_required('moderator', redirect_to='/moderator'))
    def get(self, request, *args, **kwargs):
        self.form = ArticleCategoryModelForm()
        return super(CreateArticleCategory, self).get(request, *args, **kwargs)

    @method_decorator(login_required(login_url='/login'))
    @method_decorator(group_required('moderator', redirect_to='/moderator'))
    def post(self, request, *args, **kwargs):
        article_category = ArticleCategoryModelForm(request.POST)
        if article_category.is_valid():
            article_category.save()
            MessageManager().makeMessage(request, message='success_created')
            return redirect(request.META.get('HTTP_REFERER'))
        MessageManager().makeMessage(request, message='problem_with_save')
        return redirect(str(request.path))

    def get_context_data(self, **kwargs):
        context = super(CreateArticleCategory, self).get_context_data(**kwargs)
        context['article_category_form'] = self.form
        return context


class EditArticleCategory(TemplateView):
    template_name = 'articlecategory/edit_article_category.html'

    @method_decorator(login_required(login_url='/login'))
    @method_decorator(group_required('moderator', redirect_to='/moderator'))
    def get(self, request, *args, **kwargs):
        article_category = ArticleCategory.objects.get(pk = kwargs['article_category_pk'])
        self.form = ArticleCategoryModelForm(instance = article_category)
        return super(EditArticleCategory, self).get(request, *args, **kwargs)

    @method_decorator(login_required(login_url='/login'))
    @method_decorator(group_required('moderator', redirect_to='/moderator'))
    def post(self, request, *args, **kwargs):
        article_category = ArticleCategory.objects.get(pk = kwargs['article_category_pk'])
        edited_article_category = ArticleCategoryModelForm(request.POST, instance=article_category)
        if edited_article_category.is_valid():
            edited_article_category.save()
            MessageManager().makeMessage(request, message='success_edited')
            return redirect(request.META.get('HTTP_REFERER'))
        MessageManager().makeMessage(request, message='problem_with_save')
        return redirect(str(request.path))

    def get_context_data(self, **kwargs):
        context = super(EditArticleCategory, self).get_context_data(**kwargs)
        context['article_category_form'] = self.form
        return context


@method_decorator(login_required(login_url='/login'))
@method_decorator(group_required('moderator', redirect_to='/moderator'))
def removeArticleCategory(request, *args, **kwargs):
    if request.method == 'POST':
        article_category = ArticleCategory.objects.get(pk = kwargs['article_category_pk'])
        article_category.delete()
        return redirect(str(request.path))


class GetArticleCategories(TemplateView):
    template_name = 'articlecategory/get_article_categories.html'

    @method_decorator(login_required(login_url='/login'))
    @method_decorator(group_required('moderator', redirect_to='/moderator'))
    def get(self, request, *args, **kwargs):
        self.article_categoies = ArticleCategory.objects.all()
        return super(GetArticleCategories, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GetArticleCategories, self).get_context_data(**kwargs)
        context['article_categories'] = self.article_categoies
        return context


def getArticleCategories(request, *args, **kwargs):
    if request.method == 'GET':
        article_categories = ArticleCategoryManager().get_article_categories(request)
#        article_categories = serialize('json', article_categories)
        collect_article_categories = {}
        index = 0
        for article_category in article_categories:
            collect_article_categories[index] = Collect(name = article_category.name, value = article_category.pk).obj
            index += 1
        collect_article_categories = json.dumps(collect_article_categories)
        return HttpResponse(collect_article_categories, content_type = 'application/json')
    return HttpResponse('501')