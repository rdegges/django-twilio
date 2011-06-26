"""Test suite for django-twilio."""


from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from .decorators import twilio_view


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

		# These are fake HttpRequest objects that we'll use to mimick twilio
		# responses.
		self.request_get = HttpRequest()
		self.request_get.method = 'GET'
		self.request_post = HttpRequest()
		self.request_post.method = 'POST'

	def test_forgery_returns_forbidden(self):
		"""Ensure that forged twilio requests are dealt with properly."""
		response = twilio_view(self.str_view)(self.request_post)
		self.assertEquals(response.status_code, 403)

	def test_forgery_check_allows_real_requests(self):
		"""Ensure that real twilio requests are allowed through."""
		pass

	def test_is_csrf_exempt(self):
		"""Ensure a wrapped view is exempt from CSRF checks."""
		response = twilio_view(self.str_view)(self.request_post)
		self.assertTrue(response.csrf_exempt)

	def test_allows_post(self):
		"""Ensure a wrapped view accepts POST requests."""
		response = twilio_view(self.str_view)(self.request_post)
		self.assertTrue(response.status_code != 405)

	def test_requires_post(self):
		"""Ensure a wrapped view requires POST requests."""
		response = twilio_view(self.str_view)(self.request_get)
		self.assertEquals(response.status_code, 405)

	def test_httpresponse_pass_through(self):
		"""Ensure that if a wrapped view returns a HttpResponse object then we
		don't modify the response.
		"""
		response = twilio_view(self.response_view)(self.request_post)
		self.assertTrue(isinstance(response, HttpResponse))

	def test_str_is_modified(self):
		"""Ensure that we create a HttpResponse object for the developer if the
		wrapped view returns a string.
		"""
		response = twilio_view(self.str_view)(self.request_post)
		self.assertTrue(isinstance(response, HttpResponse))
