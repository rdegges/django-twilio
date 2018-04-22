# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from . import views

# Test URLs for our ``django_twilio.decorators`` module.
urlpatterns = [
    url(r'^decorators/response_view/$', views.response_view),
    url(r'^decorators/response_class_view/$', views.ResponseView.as_view()),
    url(r'^decorators/str_view/$', views.str_view),
    url(r'^decorators/str_class_view/$', views.StrView.as_view()),
    url(r'^decorators/bytes_view/$', views.bytes_view),
    url(r'^decorators/bytes_class_view/$', views.BytesView.as_view()),
    url(r'^decorators/verb_view/$', views.verb_view),
    url(r'^decorators/verb_class_view/$', views.VerbView.as_view())
]