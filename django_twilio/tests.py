"""Test suite for django-twilio."""


from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from django.contrib.sites.models import get_current_site

from .decorators import twilio_view


class TwilioViewTestCase(TestCase):
	"""Run tests against the ``twilio_view`` decorator."""

	def setUp(self):
		# Store our test domain for mocking twilio forgery protection.
		self.domain = get_current_site(self.request_post).domain

	def test_is_csrf_exempt(self):
		response = twilio_view(str_view)(self.request_post)
		self.assertTrue(response.csrf_exempt)

	def test_requires_post(self):
		response = twilio_view(str_view)(self.request_get)
		self.assertEquals(response.status_code, 405)

	def test_decorator_preserves_metadata(self):
		view = twilio_view(str_view)
		self.assertEqual(view.__name__, 'str_view')

	def test_forged_requests_return_forbidden(self):
		response = twilio_view(str_view)(self.request_post)
		self.assertEquals(response.status_code, 403)

	def test_forgery_check_allows_real_requests(self):
		"""Ensure that real twilio requests are allowed through."""
		pass

	def test_allows_post(self):
		"""Ensure a wrapped view accepts POST requests."""

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

	def test_blacklist_works(self):
		"""Ensure that blacklisted callers can't use services."""
		pass

	def test_blacklist_pass_through(self):
		"""Ensure that non-blacklisted callers can use services."""
		pass
