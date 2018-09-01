from django.shortcuts import redirect
from blacklist.models import BlackListManager


def group_required(group_name, false_function = None, redirect_to = '/'):

    #    group_name take string group name
    #    false_function have prioritet

    def wrap(function):
        def wrapped(request, *args, **kwargs):
            groups = request.user.groups.all()
            for group in groups:
                if group.name == group_name:
                    return function(request, *args, **kwargs)
            if false_function:
                return false_function
            return redirect(redirect_to)
        return wrapped
    return wrap



def email_black_list_check(false_function = None, redirect_to = None):

    def decorator(function):
        def wrapped(request, *args, **kwargs):
            exist = BlackListManager().email_exist_in_blacklist(request.user.email)
            if exist:
                if false_function:
                    return false_function
                return  redirect(redirect_to)
            return function(request, *args, **kwargs)
        return wrapped
    return decorator



def exception_redirect(func):
    def wrap(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except:
            return redirect('/crash')
    return wrap



'''
class Test(View):
    @method_decorator(group_required('admin', false_function=HttpResponse('hello')))
    def get(self, request, *rags, **kwargs):
        return HttpResponse(request.user.groups.all())
'''