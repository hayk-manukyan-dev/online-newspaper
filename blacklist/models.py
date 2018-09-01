from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

class BlackListManager(models.Manager):
    def email_exist_in_blacklist(self, email):
        try:
            black_list_object = BlackList.objects.get(email = email)
            if black_list_object.expire_in <= datetime.now():
                black_list_object.delete()
                return False
            return True
        except:
            return False

    def add_email_in_black_list(self, *args, **kwargs):
        if self.email_exist_in_blacklist(kwargs['email']) != True:
            black_email = self.create(**kwargs)
            return black_email
        raise ValueError('(BlackListManager > add_email_in_black_list) email is exist in blacklist')


class BlackList(models.Model):
    by = models.ForeignKey(get_user_model(), null=True, on_delete = models.SET_NULL)
    email = models.EmailField(unique=True)
    reason = models.CharField(max_length=2000, null=True, blank=True)
    date = models.DateField(auto_now_add = True)
    expire_in = models.DateField(null = True, blank = True)

    objects = BlackListManager()
