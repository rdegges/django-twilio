from django.conf.urls.defaults import patterns, url


# Test URLs for our ``django_twilio.decorators`` module.
urlpatterns = patterns('django_twilio.tests.views',
    url(r'^tests/decorators/response_view/$', 'response_view'),
    url(r'^tests/decorators/str_view/$', 'str_view'),
    url(r'^tests/decorators/verb_view/$', 'verb_view'),
)
