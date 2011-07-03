from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('django_twilio.tests.views',
	url(r'^test/response_view/$', 'response_view'),
	url(r'^test/str_view/$', 'str_view'),
	url(r'^test/verb_view/$', 'verb_view'),
)
