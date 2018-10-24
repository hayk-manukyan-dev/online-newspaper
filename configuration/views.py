from django.shortcuts import HttpResponse, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from processing.base.decorators import group_required, exception_redirect

from configuration.transfers import readJson, writeJson, mixedArticlesSave, getMemoryJsonData
from processing.base.managers import MessageManager, Collect

import json


class MixedArticlesConfig(View):

    @method_decorator(exception_redirect)
    @method_decorator(login_required)
    @method_decorator(group_required('admin', HttpResponse(MessageManager().getMessage(message = 'no_privileg_to_reach_this_page'))))
    def get(self, request, *args, **kwargs):
        mixed_articles = readJson('configuration/json/webconfig.json')['mixed_articles']
        return HttpResponse(json.dumps(mixed_articles), content_type = 'application/json')

    @method_decorator(exception_redirect)
    @method_decorator(login_required)
    @method_decorator(group_required('admin', HttpResponse(MessageManager().getMessage(message = 'no_privileg_to_reach_this_page'))))
    def post(self, request, *args, **kwargs):
        if request.FILES['mixed_articles'].name[-5:] == '.json':
            data = getMemoryJsonData(request.FILES['mixed_articles'])
            web_config = readJson('configuration/json/webconfig.json')
            web_config['mixed_articles'] = data
            write_to_file = writeJson('configuration/json/webconfig.json', web_config)
            if write_to_file:
                MessageManager().makeMessage(request, message = 'success_edited')
                return redirect(request.META.get('HTTP_REFERER'))
            MessageManager().makeMessage(request, message = 'problem_with_save')
            return redirect(request.META.get('HTTP_REFERER'))
        MessageManager().makeMessage(request, message = 'unsupported_file_type')
        return redirect(request.META.get('HTTP_REFERER'))
