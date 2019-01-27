from processing.base.managers import Collect


def collectUsers(users):
    collect_user = {}
    iterate_user = 0
    for user in users:
        collect_user[iterate_user] = Collect(pk = user.pk).obj
        date_joined = str(user.date_joined.date()) + ' ' + str(user.date_joined.hour) + ':' + str(user.date_joined.hour)
        collect_user[iterate_user]['fields'] = Collect(first_name = user.first_name, last_name = user.last_name, email = user.email, email_confirmed = user.email_confirmed, avatar = str(user.avatar), is_superuser = user.is_superuser, is_staff = user.is_staff, is_active= user.is_active, date_joined = str(date_joined), groups = {}).obj
        iterate_group = 0
        for group in user.groups.all():
            collect_user[iterate_user]['fields']['groups'][iterate_group] = Collect(name = group.name, pk = group.pk).obj
            iterate_group += 1
        iterate_user += 1
    return collect_user
