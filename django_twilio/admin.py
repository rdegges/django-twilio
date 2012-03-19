"""This module provides useful django admin hooks that allow you to manage
various components through the django admin panel (if enabled).
"""

from django.contrib import admin

from django_twilio.models import Caller


class CallerAdmin(admin.ModelAdmin):
    """This class provides admin panel integration for our
    :class:`django_twilio.models.Caller` model.
    """
    list_display = ('__unicode__', 'blacklisted')


admin.site.register(Caller, CallerAdmin)
