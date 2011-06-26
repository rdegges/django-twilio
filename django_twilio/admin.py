"""This module provides useful django admin hooks that allow you to manage
various components through the django admin panel (if enabled).
"""

from django.contrib import admin

from .models import Caller


class CallerAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'blacklisted')


admin.site.register(Caller, CallerAdmin)
