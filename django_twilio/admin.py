# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
This module provides useful django admin hooks that allow you to manage
various components through the django admin panel (if enabled).
"""

from django.contrib import admin

from .models import Caller, Credential


class CallerAdmin(admin.ModelAdmin):
    """This class provides admin panel integration for our
    :class:`django_twilio.models.Caller` model.
    """
    list_display = ('__str__', 'blacklisted')


admin.site.register(Caller, CallerAdmin)
admin.site.register(Credential)
