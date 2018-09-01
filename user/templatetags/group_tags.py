from django.contrib.auth.models import Group
from django import template


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        if group in user.groups.all():
            return True
        return False
    except:
        return False
