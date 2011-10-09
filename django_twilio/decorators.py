"""Useful decorators."""


from functools import wraps

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseForbidden

from twilio.twiml import Verb
from twilio.util import RequestValidator

def twilio_view(f):
	"""This decorator provides several helpful shortcuts for writing twilio
	views.

		- It ensures that only requests from twilio are passed through. This
		  helps protect you from forged requests.

		- It ensures  your view is exempt from CSRF checks via Django's
		  @csrf_exempt decorator. This is necessary for any view that accepts
		  POST requests from outside the local domain (eg: twilio's servers).

		- It allows your view to (optionally) return TwiML to pass back to
		  twilio's servers instead of building a HttpResponse object manually.

		  .. note::
			At this time this ONLY supports XML TwiML since the twilio
			library only supports XML rendering at the moment. In future
			releases this may be changed to support JSON (and other formats) as
			well.

	Usage::

		from twilio import Response, Sms

		@twilio_view
		def my_view(request):
			r = Response()
			r.append(Sms('Thanks for the SMS message!'))
			return r
	"""
	@csrf_exempt
	@require_POST
	@wraps(f)
	def decorator(request, *args, **kwargs):
		# Here we'll use the twilio library's request validation code to ensure
		# that the current request actually came from twilio, and isn't a
		# forgery. If it is a forgery, then we'll return a HTTP 403 error
		# (forbidden).
		try:
			url = request.build_absolute_uri()
			signature = request.META['HTTP_X_TWILIO_SIGNATURE']
		except (AttributeError, KeyError):
			return HttpResponseForbidden()

		validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
		if not validator.validate(url, request.POST, signature):
			return HttpResponseForbidden()

		# Run the wrapped view, and capture the data returned.
		response = f(request, *args, **kwargs)

		# If the view returns a string, we'll assume it is XML TwilML data and
		# pass it back with the appropriate mimetype. We won't check the XML
		# data because that would be too time consuming for every request.
		# Instead, we'll let the errors pass through to be dealt with by the
		# developer.
		if isinstance(response, Verb):
			return HttpResponse(response, mimetype='text/xml')
		else:
			return response
	return decorator
