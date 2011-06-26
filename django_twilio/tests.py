"""Test suite for django-twilio."""


from django.test import TestCase
from django.http import HttpResponse


class TwilioViewTestCase(TestCase):
	"""Run tests against the twilio_view decorator."""

	def setUp(self):
		"""Create some test helpers."""

		def test_view_that_returns_str(request):
			"""A simple test view that returns a string."""
			return '<Response><Sms>Hi!</Sms></Response>'
		self.str_view = test_view_that_returns_str

		def test_view_that_returns_httpresponse(request):
			"""A simple test view that returns a HttpResponse object."""
			return HttpResponse('<Response><Sms>Hi!</Sms></Response>',
					mimetype='text/xml')
		self.response_view = test_view_that_returns_httpresponse


	def test_forgery_returns_forbidden(self):
		"""Ensure that forged twilio requests are dealt with properly."""
		pass

	def test_forgery_check_allows_real_requests(self):
		"""Ensure that real twilio requests are allowed through."""
		pass

	def test_is_csrf_exempt(self):
		"""Ensure a wrapped view is exempt from CSRF checks."""
		pass

	def test_allows_post(self):
		"""Ensure a wrapped view accepts POST requests."""
		pass

	def test_requires_post(self):
		"""Ensure a wrapped view requires POST requests."""
		pass
