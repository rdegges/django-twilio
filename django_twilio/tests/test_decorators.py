from hmac import new
from hashlib import sha1
from base64 import encodestring

from django.conf import settings
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase

from django_twilio.tests.views import response_view, str_view, verb_view


class TwilioViewTestCase(TestCase):
	"""Run tests against the ``twilio_view`` decorator."""
	fixtures = ['django_twilio.json']
	urls = 'django_twilio.tests.urls'

	def setUp(self):
		self.client = Client(enforce_csrf_checks=True)
		self.factory = RequestFactory(enforce_csrf_checks=True)

		# Test URI.
		self.uri = 'http://testserver/tests'

		# Guarantee a value for the required configuration settings after each
		# test case.
		settings.TWILIO_ACCOUNT_SID = 'xxx'
		settings.TWILIO_AUTH_TOKEN = 'xxx'

		# Pre-calculate twilio signatures for our two test views.
		self.response_signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
				'%s/response_view/' % self.uri, sha1).digest()).strip()
		self.str_signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
				'%s/str_view/' % self.uri, sha1).digest()).strip()
		self.str_signature_with_from_field_normal_caller = encodestring(new(
				settings.TWILIO_AUTH_TOKEN,
				'%s/str_view/From+12222222222' % self.uri,
				sha1).digest()).strip()
		self.str_signature_with_from_field_blacklisted_caller = encodestring(
				new(settings.TWILIO_AUTH_TOKEN,
				'%s/str_view/From+13333333333' % self.uri,
				sha1).digest()).strip()
		self.verb_signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
				'%s/verb_view/' % self.uri, sha1).digest()).strip()

	def test_is_csrf_exempt(self):
		self.assertTrue(self.client.post('/test/str_view/').csrf_exempt)

	def test_requires_post(self):
		self.assertEquals(self.client.get('/test/str_view/').status_code, 405)
		self.assertEquals(self.client.head('/test/str_view/').status_code, 405)
		self.assertEquals(self.client.options('/test/str_view/').status_code, 405)
		self.assertEquals(self.client.put('/test/str_view/').status_code, 405)
		self.assertEquals(self.client.delete('/test/str_view/').status_code, 405)

	def test_allows_post(self):
		request = self.factory.post('/test/str_view/',
				HTTP_X_TWILIO_SIGNATURE=self.str_signature)
		self.assertEquals(str_view(request).status_code, 200)

	def test_decorator_preserves_metadata(self):
		self.assertEqual(str_view.__name__, 'str_view')

	def test_missing_settings_return_forbidden(self):
		del settings.TWILIO_ACCOUNT_SID
		del settings.TWILIO_AUTH_TOKEN

		self.assertEquals(self.client.post('/test/str_view/').status_code, 403)

	def test_missing_signature_returns_forbidden(self):
		self.assertEquals(self.client.post('/test/str_view/').status_code, 403)

	def test_incorrect_signature_returns_forbidden(self):
		request = self.factory.post('/test/str_view/',
				HTTP_X_TWILIO_SIGNATURE='fakesignature')
		self.assertEquals(str_view(request).status_code, 403)

	def test_no_from_field(self):
		request = self.factory.post('/test/str_view/',
				HTTP_X_TWILIO_SIGNATURE=self.str_signature)
		self.assertEquals(str_view(request).status_code, 200)

	def test_from_field_no_caller(self):
		request = self.factory.post('/test/str_view/', {'From': '+12222222222'},
				HTTP_X_TWILIO_SIGNATURE=self.str_signature_with_from_field_normal_caller)
		self.assertEquals(str_view(request).status_code, 200)

	def test_blacklist_works(self):
		request = self.factory.post('/test/str_view/', {'From': '+13333333333'},
				HTTP_X_TWILIO_SIGNATURE=self.str_signature_with_from_field_blacklisted_caller)
		response = str_view(request)
		self.assertEquals(response.content, '<Response><Reject/></Response>')

	def test_decorator_modifies_str(self):
		request = self.factory.post('/test/str_view/',
				HTTP_X_TWILIO_SIGNATURE=self.str_signature)
		self.assertTrue(isinstance(str_view(request), HttpResponse))

	def test_decorator_modifies_verb(self):
		request = self.factory.post('/test/verb_view/',
				HTTP_X_TWILIO_SIGNATURE=self.verb_signature)
		self.assertTrue(isinstance(verb_view(request), HttpResponse))

	def test_decorator_preserves_httpresponse(self):
		request = self.factory.post('/test/response_view/',
				HTTP_X_TWILIO_SIGNATURE=self.response_signature)
		self.assertTrue(isinstance(response_view(request), HttpResponse))

#	def test_blacklist_works(self):
#		"""Ensure that blacklisted callers can't use services."""
#		c = Caller.objects.get(phone_number='+16666666666')
#		self.assertTrue(c.blacklisted)
#
#		response = twilio_view(str_view)(self.request_blacklisted_caller)
#		self.assertEquals(response.status_code, 200)
#		self.assertEquals(response.content, '<Response><Reject/></Response>')
#
#	def test_blacklist_pass_through(self):
#		"""Ensure that non-blacklisted callers can use services."""
#		c = Caller.objects.get(phone_number='+15555555555')
#		self.assertFalse(c.blacklisted)
#
#		response = twilio_view(str_view)(self.request_caller)
#		self.assertTrue(response.content != '<Response><Reject/></Response>')
