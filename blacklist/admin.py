from django.contrib import admin
from blacklist.models import BlackList

class BlackListAdmin(admin.ModelAdmin):
    list_display = ['by', 'email', 'date']

admin.site.register(BlackList, BlackListAdmin)
