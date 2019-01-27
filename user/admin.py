from django.contrib import admin
from user.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']

class BlackListAdmin(admin.ModelAdmin):
    list_display = ['email', 'date', 'pass_in']

admin.site.register(User, UserAdmin)
