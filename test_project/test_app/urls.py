# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url


# Test URLs for our ``django_twilio.decorators`` module.
urlpatterns = patterns(
    'test_project.test_app.views',
    url(r'^test_app/decorators/response_view/$', 'response_view'),
    url(r'^test_app/decorators/str_view/$', 'str_view'),
    url(r'^test_app/decorators/bytes_view/$', 'bytes_view'),
    url(r'^test_app/decorators/verb_view/$', 'verb_view'),
)
