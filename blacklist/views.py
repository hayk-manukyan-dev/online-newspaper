from django.shortcuts import render
from django.views import View


class EmailIsInBlackList(View):
    template_name = 'blacklist/email_in_blacklist.html'
    def get(self, requets, *args, **kwargs):
        return render(requets, self.template_name, {})
