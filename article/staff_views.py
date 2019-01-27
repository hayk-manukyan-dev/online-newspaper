from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from processing.base.decorators import group_required, exception_redirect
from processing.base.managers import MessageManager
from processing.base.managers import Collect

from article.models import Article
from initialarticle.models import InitialArticle

from article.staff_forms import ArticleCreateForm, ArticleEditForm



class CreateArticle(TemplateView):
    template_name = 'article/stuff/create_article.html'

    @method_decorator(exception_redirect)
    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def get(self, request, *args, **kwargs):
        self.form = ArticleCreateForm()
        self.article_language_code = kwargs['language']
        self.initialarticle = InitialArticle.objects.get(keywords = kwargs['keywords'])
        return super(CreateArticle, self).get(request, *args, **kwargs)

    @method_decorator(exception_redirect)
    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def post(self, request, *args, **kwargs):
        initial_article = InitialArticle.objects.get(keywords=kwargs['keywords'])
        self.form = ArticleCreateForm(request.POST, request.FILES)
        if self.form.is_valid():
            article_ = self.form.save_(initial_article, kwargs['language'])
            return redirect('/'+ 'article/get/' +  article_.language + '/' +str(article_.initial))
        MessageManager().makeMessage(request, message = 'form_is_not_valid')
        return redirect('x')#request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super(CreateArticle, self).get_context_data(**kwargs)
        context['article_create_form'] = self.form
        context['article_language_code'] = self.article_language_code
        context['initialarticle'] = self.initialarticle
        return  context



class EditArticle(TemplateView):
    template_name = 'article/stuff/edit_article.html'

    @method_decorator(exception_redirect)
    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def get(self, request, *args, **kwargs):
        article = Article.objects.get_article(keywords = kwargs['keywords'], language = kwargs['language'])
        if Article.objects.article_owner_is_requester(request, article):
            self.form = ArticleEditForm(instance = article)
            self.article_language_code = kwargs['language']
            self.initialarticle = InitialArticle.objects.get(keywords=kwargs['keywords'])
            return super(EditArticle, self).get(request, *args, **kwargs)
        MessageManager().makeMessage(request, message = 'no_privileg_to_reach_this_page')
        return redirect(request.META.get('HTTP_REFERER'))

    @method_decorator(exception_redirect)
    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def post(self, request, *args, **kwargs):
        article = Article.objects.get_article(keywords = kwargs['keywords'], language = kwargs['language'])
        if Article.objects.article_owner_is_requester(request, article):
            self.form = ArticleEditForm(request.POST, request.FILES, instance = article)
            if self.form.is_valid():
                article = self.form.edit(article)
                return redirect('/article/get/' + article.language + '/' + article.initial.keywords)
            MessageManager().makeMessage(request, message = 'form_is_not_valid')
            return redirect('x')#request.META.get('HTTP_REFERER'))
        MessageManager().makeMessage(request, message = 'no_privileg_to_reach_this_page')
        return redirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super(EditArticle, self).get_context_data(**kwargs)
        context['article_edit_form'] = self.form
        context['article_language_code'] = self.article_language_code
        context['initialarticle'] = self.initialarticle
        return  context


def removeArticle(request, *args, **kwargs):
    if request.method == 'POST':
        article = Article.objects.get_article(keywords = kwargs['keywords'], language = kwargs['language'])
        if Article.objects.article_owner_is_requester(request, article):
            article.delete()
            return HttpResponse(Collect(success=True).get_json(), content_type='application/json')
        return HttpResponse(Collect(success=False, message=MessageManager().getMessage(message='no_privileg_to_reach_this_page')).get_json(), content_type='application/json')
    return HttpResponse('501')
