from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('django_twilio.tests.views',
	# Test URLs for our ``django_twilio.decorators`` module.
	url(r'^tests/response_view/$', 'response_view'),
	url(r'^tests/str_view/$', 'str_view'),
	url(r'^tests/verb_view/$', 'verb_view'),
)
