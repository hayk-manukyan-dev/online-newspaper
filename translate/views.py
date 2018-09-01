from django.shortcuts import redirect, HttpResponse
from django.utils import translation
from online_newspaper.settings import languages_dict


def changeLanguage(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['language'] in languages_dict:
            translation.activate(kwargs['language'])
            request.session[translation.LANGUAGE_SESSION_KEY] = kwargs['language']
            return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('404')

