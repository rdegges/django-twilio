# -*- coding: utf-8 -*-

from django.urls import path

from . import views

# Test URLs for our ``django_twilio.decorators`` module.
urlpatterns = [
    path('decorators/response_view/', views.response_view),
    path('decorators/response_class_view/', views.ResponseView.as_view()),
    path('decorators/str_view/', views.str_view),
    path('decorators/str_class_view/', views.StrView.as_view()),
    path('decorators/bytes_view/', views.bytes_view),
    path('decorators/bytes_class_view/', views.BytesView.as_view()),
    path('decorators/verb_view/', views.verb_view),
    path('decorators/verb_class_view/', views.VerbView.as_view())
]