from django.test import Client
from django.test import TestCase


class TwilioViewTestCase(TestCase):
	"""Run tests against the ``twilio_view`` decorator."""
	fixtures = ['caller_blacklist.json']
	urls = 'django_twilio.tests.urls'

	def setUp(self):
		self.client = Client(enforce_csrf_checks=True)

	def test_is_csrf_exempt(self):
		response = self.client.post('/test/str_view/')
		self.assertTrue(response.csrf_exempt)

#	def test_requires_post(self):
#		response = self.client.get('/test/str_view/')
#		self.assertEquals(response.status_code, 405)
#
#	def test_decorator_preserves_metadata(self):
#		view = twilio_view(str_view)
#		self.assertEqual(view.__name__, 'str_view')
#
#	def test_forged_requests_return_forbidden(self):
#		response = twilio_view(str_view)(self.request_post)
#		self.assertEquals(response.status_code, 403)
#
#	def test_forgery_check_allows_real_requests(self):
#		"""Ensure that real twilio requests are allowed through."""
#		pass
#
#	def test_allows_post(self):
#		"""Ensure a wrapped view accepts POST requests."""
#		from django.conf import settings
#		# This is a reverse engineering of the twilio forgery protection. Hey,
#		# it's the only way I could think of doing it elegantly!
#		response = self.client.post('/test/str_view/', extra={
#			'HTTP_X_TWILIO_SIGNATURE': encodestring(new(settings.TWILIO_AUTH_TOKEN, '%s/test/str_view/' % self.domain, sha1).digest()).strip()
#		})
#		self.assertTrue('HTTP_X_TWILIO_SIGNATURE' in response.META)
#		self.assertEquals(response.status_code, 200)
#
#	def test_httpresponse_pass_through(self):
#		"""Ensure that if a wrapped view returns a HttpResponse object then we
#		don't modify the response.
#		"""
#		response = twilio_view(response_view)(self.request_post)
#		self.assertTrue(isinstance(response, HttpResponse))
#
#	def test_str_is_modified(self):
#		"""Ensure that we create a HttpResponse object for the developer if the
#		wrapped view returns a string.
#		"""
#		response = twilio_view(str_view)(self.request_post)
#		self.assertTrue(isinstance(response, HttpResponse))

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
