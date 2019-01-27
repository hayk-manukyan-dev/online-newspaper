from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from blacklist.models import BlackListManager

from user.models import User, UserManager
from user.models import User

from django.contrib.auth import get_user_model
from user.models import UserManager
from django.forms.widgets import HiddenInput
from django.core.mail import send_mail
from online_newspaper.settings import ALLOWED_HOSTS


class SignUpFormValidation(BlackListManager, UserManager):
    def email_exist_in_blacklist(self, email):
        in_blacklist_exist = super(SignUpFormValidation, self).email_exist_in_blacklist(email)
        is_exist = super(SignUpFormValidation, self).find_email(email)
        if in_blacklist_exist:
            raise ValidationError(_('%(email) is exist in black list'), params={'email': email},)
        elif is_exist:
            raise ValidationError(_('%(email) is exist'), params={'email' : email})


class SignUpFormValidation(BlackListManager):
    def email_exist_in_blacklist(self, email):
        is_exist = super(SignUpFormValidation, self).email_exist_in_blacklist(email)
        if is_exist:
            raise ValidationError(_('%(email) is exist in black list'), params={'email': email},)


class SignUpForm(forms.Form):
    email = forms.CharField(label = _('Email'), validators = [SignUpFormValidation().email_exist_in_blacklist], widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder' : _('Email')}))
    first_name = forms.CharField(label = _('First Name'), max_length = 25, min_length = 2, widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder' : _('First Name')}))
    last_name = forms.CharField(label = _('Last Name'), max_length = 25, min_length = 2, widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder' : _('Last Name')}))
    password = forms.CharField(label = _('Password'), widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder' : _('Password')}))



class UserEditForm(forms.ModelForm):
    email = forms.CharField(label = _('Email'), widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder' : _('Email')}), required=False)
    first_name = forms.CharField(label = _('First Name'), max_length = 20, min_length = 2, widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder' : _('First Name')}))
    last_name = forms.CharField(label = _('Last Name'), max_length = 30, min_length = 2, widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder' : _('Last Name')}))

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit)
        if user.email != self.cleaned_data['email']:
            UserManager().save_email(user, self.cleaned_data['email'])
#            send_mail('Cnfirm Email', 'Use %s to confirm your email' % user.confirmation_key, ALLOWED_HOSTS[0], self.cleaned_data['new_email'])
        super(UserEditForm, self).save(commit)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
        exclude = ['email']



class UserAvatarForm(forms.ModelForm):
    avatar = forms.FileField(label = _('Image'))

    def __init__(self, *args, **kwargs):
        super(UserAvatarForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({'onclick' : 'editAvatarPost()'})

    def save(self, commit=True):
        user = super(UserAvatarForm, self).save(commit)
        UserManager().save_image(user, self.cleaned_data['avatar'])
        super(UserAvatarForm, self).save(commit)

    class Meta:
        model = get_user_model()
        fields = ['avatar']



class LogInForm(forms.Form):
    email = forms.CharField(label = _('Email'), validators = [SignUpFormValidation().email_exist_in_blacklist], widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder' : _('Email')}))
    password = forms.CharField(label = _('Password'), widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder' : _('Password')}))