from django.shortcuts import redirect, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, login, authenticate
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from processing.base.decorators import email_black_list_check
from processing.base.managers import MessageManager, Collect
from processing.base.captcha_result import captchaResult
from user.forms import SignUpForm, LogInForm, UserEditForm, UserAvatarForm
from user.models import UserManager
from blacklist.models import BlackListManager


class SignUp(TemplateView):
    template_name = 'user/sign_up.html'
    def get(self, request, *args, **kwargs):
        self.form = SignUpForm()
        return super(SignUp, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        recaptcha_response = captchaResult(request.POST.get('g-recaptcha-response'))
        self.form = SignUpForm(request.POST)
        if self.form.is_valid():
            if recaptcha_response['success']:
                user = get_user_model().objects.create_user(email = self.form.cleaned_data['email'], password = self.form.cleaned_data['password'], first_name = self.form.cleaned_data['first_name'], last_name = self.form.cleaned_data['last_name'])
#               send_mail(str(request.META['HTTP_HOST']) + ' Cnfirm Email', 'Use %s to confirm your email' % user.confirmation_key, str(request.META['HTTP_HOST']), [user.email])
                MessageManager().makeMessage(request, message = 'confirm_mail')
                return redirect('/')
            MessageManager().makeMessage(request, message = 'confirm_not_robot')
            return redirect(str(request.path))
        MessageManager().makeMessage(request, message = 'problem_with_sign_up')
        return redirect(str(request.path))

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['sign_up_form'] = self.form
        return context


class LogIn(TemplateView):
    template_name = 'user/log_in.html'

    def get(self, request, *args, **kwargs):
        self.form = LogInForm()
        return super(LogIn, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        recaptcha_response = captchaResult(request.POST.get('g-recaptcha-response'))
        self.form = LogInForm(request.POST)
        if self.form.is_valid():
            if recaptcha_response['success'] == False:
                user = authenticate(request, email = self.form.cleaned_data['email'], password = self.form.cleaned_data['password'])
                if user != None:
                    login(request, user)
                    MessageManager().makeMessage(request, ' '+user.first_name, message = 'wellcome')
                    return redirect('/')
                MessageManager().makeMessage(request, message='authentication_problem')
                return redirect(str(request.path))
            MessageManager().makeMessage(request, message='confirm_not_robot')
            return redirect(str(request.path))
        MessageManager().makeMessage(request, message='problem_with_log_in')
        return redirect(str(request.path))

    def get_context_data(self, **kwargs):
        context = super(LogIn, self).get_context_data(**kwargs)
        context['log_in_form'] = self.form
        return context


class LogOut(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        MessageManager().makeMessage(request, message = 'logout_successful')
        return redirect('/')


class EditUser(TemplateView):
    template_name = 'user/edit_user.html'

    @method_decorator(email_black_list_check(false_function=HttpResponse('/')))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk = request.user.pk)
        self.form = UserEditForm(instance = user)
        return super(EditUser, self).get(request, *args, **kwargs)

    @method_decorator(email_black_list_check(false_function=HttpResponse('/')))
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        recaptcha_response = captchaResult(request.POST.get('g-recaptcha-response'))
        user = get_user_model().objects.get(pk=request.user.pk)
        self.form = UserEditForm(request.POST, instance=user)
        if self.form.is_valid():
            if True:#recaptcha_response['success']:
                self.form.save()
                return redirect('/')
            MessageManager().makeMessage(request, message='confirm_not_robot')
            return redirect(str(request.path))
        MessageManager().makeMessage(request, message='problem_with_save')
        return redirect(str(request.path))

    def get_context_data(self, **kwargs):
        context = super(EditUser, self).get_context_data(**kwargs)
        context['edit_user_form'] = self.form
        return context


class UserAvatarEdit(TemplateView):
    template_name = 'user/avatar_edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.form = UserAvatarForm()
        return super(UserAvatarEdit, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.form = UserAvatarForm(request.POST, request.FILES)
        if self.form.is_valid():
            UserManager().save_image(request.user, self.form.cleaned_data['avatar'])
            return HttpResponse({'success' : 'success'}, content_type='application/json')
        MessageManager().makeMessage(request, message='problem_with_save')
        return redirect(str(request.path))

    def get_context_data(self, **kwargs):
        context = super(UserAvatarEdit, self).get_context_data(**kwargs)
        context['avatar_form'] = self.form
        return context


class UserAvatarRemove(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        remove = UserManager().remove_image(request.user)
        if bool(remove) != True:
            MessageManager().makeMessage(request, message='problem_with_save')
        return redirect(str(request.path))



#-----functions-----
@email_black_list_check(false_function=HttpResponse('/'))
@login_required
def editEmail(request):
    if request.method == 'POST':
        if request.POST['email'] != request.user.email:
            if UserManager().email_not_exist(request.POST['email']):
                if BlackListManager().email_exist_in_blacklist(request.POST['email']) != True:
                    user = get_user_model().objects.get(pk = request.user.pk)
                    save_email = UserManager().save_email(user, request.POST['email'])
                    if save_email['success']:
                        return HttpResponse(Collect(response = 'success').get_json(), content_type = 'application/json')
                    return HttpResponse(Collect(response = 'filure', message = str(MessageManager().getMessage(save_email['message']))).get_json(), content_type = 'application/json')
                return HttpResponse(Collect(response = 'filure', message = str(MessageManager().getMessage('email_is_in_black_list'))).get_json(), content_type = 'application/json')
            return HttpResponse(Collect(response = 'filure', message = str(MessageManager().getMessage('email_exist'))).get_json(), content_type = 'application/json')
        return HttpResponse('0')
    return HttpResponse('501')


@email_black_list_check(false_function=HttpResponse('/'))
@login_required
def editFirstName(request):
    if request.method == 'POST':
        try:
            user = get_user_model().objects.get(pk = request.user.pk)
            changed = UserManager().save_first_name(user, request.POST['first_name'])
            if changed['success']:
                return HttpResponse(Collect(response = 'success').get_json(), content_type = 'application/json')
            return HttpResponse(Collect(response = 'failure', message = str(MessageManager().getMessage(changed['message']))).get_json(), content_type = 'application/json')
        except:
            return HttpResponse(Collect(response = 'failure', message = str(MessageManager().getMessage('problem_with_save'))).get_json(), content_type = 'application/json')
    return HttpResponse('501')


@email_black_list_check(false_function=HttpResponse('/'))
@login_required
def editLastName(request):
    if request.method == 'POST':
        try:
            user = get_user_model().objects.get(pk = request.user.pk)
            changed = UserManager().save_last_name(user, request.POST['last_name'])
            if changed['success']:
                return HttpResponse(Collect(response = 'success').get_json(), content_type = 'application/json')
            return HttpResponse(Collect(response = 'failure', message = str(MessageManager().getMessage(changed['message']))).get_json(), content_type = 'application/json')
        except:
            return HttpResponse(Collect(response = 'failure', message = str(MessageManager().getMessage('problem_with_save'))).get_json(), content_type = 'application/json')
    return HttpResponse('501')


@email_black_list_check(false_function=HttpResponse('/'))
@login_required
def editAvatar(request):
    if request.method == 'POST':
        try:
            print(request.FILES['avatar'])
            if request.FILES:
                UserManager().save_image(request.user, request.FILES['avatar'])
                return HttpResponse(Collect(response = 'success').get_json(), content_type = 'application/json')
            return HttpResponse(Collect(response='failure', message=str(MessageManager().getMessage('problem_with_save'))).get_json, content_type='application/json')
        except:
            return HttpResponse(Collect(response='failure', message=str(MessageManager().getMessage('problem_with_save'))).get_json, content_type='application/json')
    return HttpResponse('501')
