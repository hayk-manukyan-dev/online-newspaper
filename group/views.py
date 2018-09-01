from django.shortcuts import redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from processing.base.decorators import group_required
from processing.base.managers import MessageManager


@login_required
@group_required('admin', redirect_to='none')
def addUserToGroup(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            user = get_user_model().objects.get(pk = kwargs['user_pk'])
            group = Group.objects.get(pk = kwargs['group_pk'])
            group.user_set.add(user)
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            MessageManager().makeMessage(request, message = 'problem_with_save')
            return redirect(str(request.path))
    return HttpResponse('501')


@login_required
@group_required('admin', redirect_to='none')
def removeUserFromGroup(request, *args, **kwargs):
    if request.method == 'GET':
#        try:

        user = get_user_model().objects.get(pk = kwargs['user_pk'])
        group = Group.objects.get(pk=kwargs['group_pk'])
        group.user_set.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))
#        except:
#            MessageManager().makeMessage(request, message = 'problem_with_save')
#            return redirect(request.META.get('HTTP_REFERER'))
#    return HttpResponse('501')
