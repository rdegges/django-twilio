from django.contrib import admin

from .models import Caller


class CallerAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'blacklisted')


admin.site.register(Caller, CallerAdmin)
