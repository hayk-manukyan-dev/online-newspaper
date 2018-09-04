from django.shortcuts import redirect, HttpResponse

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from processing.base.decorators import group_required
from processing.base.managers import MessageManager
from processing.base.managers import Collect

from initialarticle.models import InitialArticle

from initialarticle.forms import InitialArticleCreateForm, InitialArticleEditForm




class CreateInitialArticle(TemplateView):
    template_name = 'initialarticle/create_initial_article.html'

    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def get(self, request, *args, **kwargs):
        self.form = InitialArticleCreateForm(request = request)
        return super(CreateInitialArticle, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def post(self, request, *args, **kwargs):
        self.form = InitialArticleCreateForm(request.POST, request = request)
        if self.form.is_valid():
            initial_aticle = self.form.save(request.user)
            return redirect('/article/stuff/create/'+ request.LANGUAGE_CODE +'/' + str(initial_aticle.keywords))
        MessageManager().makeMessage(request, message = 'form_is_not_valid')
        return redirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super(CreateInitialArticle, self).get_context_data(**kwargs)
        context['create_initial_article_fileds'] = self.form
        return context



class EditInitialArticle(TemplateView):
    template_name = 'initialarticle/edit_initial_article.html'

    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def get(self, request, *args, **kwargs):
        initial_article = InitialArticle.objects.get_by_keywords(keywords = kwargs['keywords'])
        if InitialArticle.objects.initial_article_owner_is_requester(request, initial_article):
            self.form = InitialArticleEditForm(instance = initial_article, request = request)
            return super(EditInitialArticle, self).get(request, *args, **kwargs)
        MessageManager().makeMessage(request, message = 'no_privileg_to_reach_this_page')
        return redirect(request.META.get('HTTP_REFERER'))

    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def post(self, request, *args, **kwargs):
        initial_article = InitialArticle.objects.get_by_keywords(keywords = kwargs['keywords'])
        if InitialArticle.objects.initial_article_owner_is_requester(request, initial_article):
            self.form = InitialArticleEditForm(request.POST, instance = initial_article, request = request)
            if self.form.is_valid():
                new_initial_article = self.form.save_(article_keywords_object = initial_article, user = request.user)
                return redirect('/initialarticle/userarticles')
            MessageManager().makeMessage(request, message='form_is_not_valid')
            return redirect(request.META.get('HTTP_REFERER'))
        MessageManager().makeMessage(request, message = 'no_privileg_to_reach_this_page')
        return redirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super(EditInitialArticle, self).get_context_data(**kwargs)
        context['edit_initial_article_fileds'] = self.form
        return context


def removeInitialArticle(request, *args, **kwargs):
    if request.method == 'GET':
        initial_article = InitialArticle.objects.get(keywords = kwargs['keywords'])
        if InitialArticle.objects.initial_article_owner_is_requester(request, initial_article):
            initial_article.delete()
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.path_info)
    return HttpResponse('501')


class RequesterInitialarticles(TemplateView):
    template_name = 'initialarticle/requester_initilarticles.html'
    @method_decorator(login_required)
    @method_decorator(group_required('stuff'))
    def get(self, request, *args, **kwargs):
        self.initialarticles = InitialArticle.objects.filter(by = request.user)
        return super(RequesterInitialarticles, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequesterInitialarticles, self).get_context_data(**kwargs)
        context['initialarticles'] = self.initialarticles
        return context

