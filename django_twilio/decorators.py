# -*- coding: utf-8 -*-

"""Useful decorators."""


from functools import wraps

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed)

from twilio.twiml import Verb
from twilio.util import RequestValidator

from django_twilio import settings as django_twilio_settings
from django_twilio.utils import get_blacklisted_response


def twilio_view(f):
    """This decorator provides several helpful shortcuts for writing Twilio
    views.

        - It ensures that only requests from Twilio are passed through. This
          helps protect you from forged requests.

        - It ensures your view is exempt from CSRF checks via Django's
          @csrf_exempt decorator. This is necessary for any view that accepts
          POST requests from outside the local domain (eg: Twilio's servers).

        - It enforces the blacklist. If you've got any ``Caller``s who are
          blacklisted, any requests from them will be rejected.

        - It allows your view to (optionally) return TwiML to pass back to
          Twilio's servers instead of building a ``HttpResponse`` object
          manually.

        - It allows your view to (optionally) return any ``twilio.Verb`` object
          instead of building a ``HttpResponse`` object manually.

          .. note::
            The forgery protection checks ONLY happen if ``settings.DEBUG =
            False`` (aka, your site is in production).

    Usage::

        from twilio.twiml import Response

        @twilio_view
        def my_view(request):
            r = Response()
            r.message('Thanks for the SMS message!')
            return r
    """
    @csrf_exempt
    @wraps(f)
    def decorator(request_or_self, methods=['POST'],
                  blacklist=True, *args, **kwargs):

        class_based_view = not(isinstance(request_or_self, HttpRequest))
        if not class_based_view:
            request = request_or_self
        else:
            assert len(args) >= 1
            request = args[0]

        # Turn off Twilio authentication when in debug mode otherwise
        # things do not work properly. For more information see the docs
        if not settings.DEBUG:

            if request.method not in methods:
                return HttpResponseNotAllowed(request.method)

            # Forgery check
            try:
                validator = RequestValidator(
                    django_twilio_settings.TWILIO_AUTH_TOKEN)
                url = request.build_absolute_uri()
                signature = request.META['HTTP_X_TWILIO_SIGNATURE']
            except (AttributeError, KeyError):
                return HttpResponseForbidden()

            if request.method == 'POST':
                if not validator.validate(url, request.POST, signature):
                    return HttpResponseForbidden()
            if request.method == 'GET':
                if not validator.validate(url, request.GET, signature):
                    return HttpResponseForbidden()

        # Blacklist check
        if blacklist:
            blacklisted_resp = get_blacklisted_response(request)
            if blacklisted_resp:
                return blacklisted_resp

        response = f(request_or_self, *args, **kwargs)

        if isinstance(response, str):
            return HttpResponse(response, content_type='application/xml')
        elif isinstance(response, Verb):
            return HttpResponse(str(response), content_type='application/xml')
        else:
            return response
    return decorator
