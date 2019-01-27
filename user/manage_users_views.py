from django.shortcuts import redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from processing.base.decorators import group_required
from processing.base.managers import MessageManager


class AddUserInGroup(View):

    @method_decorator(login_required(login_url = 'login'))
    @method_decorator(group_required('admin', redirect_to='/'))
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk = kwargs['user_pk'])
        groups = Group.objects.exclude(name = 'admin')
        for group in groups:
            if group.name == kwargs['group']:
                group.user_set.add(user)
                return redirect(request.META.get('HTTP_REFERER'))
        MessageManager().makeMessage(request, message = 'group_not_exist')
        return redirect(request.META.get('HTTP_REFERER'))



class RemoveUserFromGroup(View):

    @method_decorator(login_required(login_url = 'login'))
    @method_decorator(group_required('admin', redirect_to='/'))
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk = kwargs['user_pk'])
        groups = Group.objects.exclude(name = 'admin')
        for group in groups:
            if group.name == kwargs['group']:
                group.user_set.remove(user)
                return redirect(request.META.get('HTTP_REFERER'))
        MessageManager().makeMessage(request, message = 'group_not_exist')
        return redirect(request.META.get('HTTP_REFERER'))



class GetUsers(TemplateView):
    template_name = 'manage/manage_users.html'

    @method_decorator(login_required(login_url = 'login'))
    @method_decorator(group_required('admin', redirect_to='/'))
    def get(self, request, *args, **kwargs):
        self.users = get_user_model().objects.exclude(groups__name = 'admin')
        return super(GetUsers, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GetUsers, self).get_context_data(**kwargs)
        context['users'] = self.users
        return context

