from django.shortcuts import redirect
from django.views.generic import View

class EnteryLanguageDetect(View):
    def get(self, request, *args, **kwargs):
        return redirect('/' + request.LANGUAGE_CODE)