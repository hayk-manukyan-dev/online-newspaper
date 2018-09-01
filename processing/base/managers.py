import json

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class Collect:
    def __init__(self, *args, **kwargs):
        self.obj = {}
        for kwarg in kwargs:
            if type(kwargs[kwarg]) == None:
                kwargs[kwarg] = "none"
            self.obj[kwarg] = kwargs[kwarg]

    def get_object(self):
        return self.obj

    def get_json(self):
        return json.dumps(self.obj)



class MessageManager(object):
    def messagesDict(self):
        return {
            "confirm_mail": [_("Email isn't confirmed, please confirm it"), messages.info],
            "email_exist" : [_("Email is using, please try another one"), messages.info],
            "email_validation_failure" : ["Email isn't valid, enter valid mail", messages.error],
            "confirm_not_robot": [_("Please confirm <I'm Not a Robot> fild"), messages.warning],
            "length_error" : [_("Entered fild is not enogth long please type 2 or more letters"), messages.info],
            "problem_with_sign_up": [
                _("Somthing went wrong, account was not created. Look here for additional information"),
                messages.warning],
            "wellcome": [_("Wellcome"), messages.success],
            "authentication_problem": [_("Account is not exist"), messages.warning],
            "problem_with_log_in": [
                _('Somthing went wrong, login was not applied. Look here for additional information'),
                messages.warning],
            "problem_with_save" : [_("Somthing went wrong, please try again"), messages.warning],
            "form_is_not_valid" : [_("Entered som characters or field is not valid please check fields and try again to save"), messages.warning],
            "logout_successful" : [_("Success log outed"), messages.info],
            "no_privileg_to_reach_this_page" : [_("You has no privileg to reach this page"), messages.error],
            "group_not_exist" : [_("Group is not exist or not possible to set"), messages.error],

            "success_created" : [_('Success created'), messages.info],
            "success_edited" : [_("Success edited"), messages.info],
            "True": ["True", True, messages.success],
            "False": ["False", False, messages.error],

        }

    def makeMessage(self, request, *args, **kwargs):
        if kwargs['message']:
            message_dict = self.messagesDict()
            processed_message = message_dict[kwargs['message']][0]
            for arg in args:
                processed_message += str(arg)
            message_tag = message_dict[kwargs['message']][1]
            message_tag(request, processed_message)
            return True
        return False

    def getMessage(self, message):
        message_dict = self.messagesDict()
        return message_dict[message][0]
