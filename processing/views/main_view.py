from django.shortcuts import redirect
from django.views.generic import View
from django.utils.translation import get_language

class EnteryLanguageDetect(View):
    def get(self, request, *args, **kwargs):
        return redirect('/' + get_language())