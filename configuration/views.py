from django.shortcuts import HttpResponse
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
    @method_decorator(group_required('admin'))
    def get(self, request, *args, **kwargs):
        mixed_articles = readJson('configuration/json/webconfig.json')['mixed_articles']
        return HttpResponse(json.dumps(mixed_articles), content_type = 'application/json')

    @method_decorator(exception_redirect)
    @method_decorator(login_required)
    @method_decorator(group_required('admin'))
    def post(self, request, *args, **kwargs):
        if request.FILES['mixed_articles'].name[-5:] == '.json':
            data = getMemoryJsonData(request.FILES['mixed_articles'])
            web_config = readJson('configuration/json/webconfig.json')
            web_config['mixed_articles'] = data
            write_to_file = writeJson('configuration/json/webconfig.json', web_config)
            if write_to_file:
                return HttpResponse(Collect(response='success').get_json(), content_type='application/json')
            return HttpResponse(Collect(response = 'filure', message = str(MessageManager().getMessage('problem_with_save'))).get_json(), content_type='application/json')
        return HttpResponse(Collect(response = 'filure', message = str(MessageManager().getMessage('problem_with_save'))).get_json(), content_type='application/json')
