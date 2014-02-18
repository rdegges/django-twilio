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


def simple_twilio_view(f):
    '''
        Sometimes twilio_view will not work properly with tunnels or other
        server configurations (like ngrok).
        simple_twilio_view provides the bare minimum view that returns a
        TWiML response with the correct HTTP headers.
        It will also prevent any HTTP verb other than POST.

        NEVER use simple_twilio_view in production: use twilio_view instead.

    '''
    @csrf_exempt
    @wraps(f)
    def decorator(request_or_self, methods=['POST'], *args, **kwargs):
        class_based_view = not (isinstance(request_or_self, HttpRequest))
        if not class_based_view:
            request = request_or_self
        else:
            assert len(args) >= 1
            request = args[0]

        if request.method not in methods:
            return HttpResponseNotAllowed(request.method)

        response = f(request_or_self, *args, **kwargs)

        if isinstance(response, str):
            return HttpResponse(response, mimetype='application/xml')
        elif isinstance(response, Verb):
            return HttpResponse(str(response), mimetype='application/xml')
        else:
            return response
    return decorator


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

        class_based_view = not (isinstance(request_or_self, HttpRequest))
        if not class_based_view:
            request = request_or_self
        else:
            assert len(args) >= 1
            request = args[0]

        # Only handle Twilio forgery protection stuff if we're running in
        # production. This way, developers can test their Twilio view code
        # without getting errors.
        if not settings.DEBUG:

            # Attempt to gather all required information to allow us to check
            # the incoming HTTP request for forgery. If any of this information
            # is not available, then we'll throw a HTTP 403 error (forbidden).
            #
            # The required fields to check for forged requests are:
            #
            #   1. ``TWILIO_ACCOUNT_SID`` (set in the site's settings module).
            #   2. ``TWILIO_AUTH_TOKEN`` (set in the site's settings module).
            #   3. The full URI of the request, eg:
            #      'http://mysite.com/test/view/'.
            #      This may not necessarily be available if this view is being
            #      called via a unit testing library, or in certain localized
            #      environments.
            #   4. A special HTTP header, ``HTTP_X_TWILIO_SIGNATURE`` which
            #      contains a hash that we'll use to check for forged requests.
            if request.method not in methods:
                return HttpResponseNotAllowed(request.method)

            # Validate the request
            try:
                validator = RequestValidator(
                    django_twilio_settings.TWILIO_AUTH_TOKEN)
                url = request.build_absolute_uri()
                signature = request.META['HTTP_X_TWILIO_SIGNATURE']
            except (AttributeError, KeyError):
                return HttpResponseForbidden()

            # Now that we have all the required information to perform forgery
            # checks, we'll actually do the forgery check.
            if request.method == 'POST':
                if not validator.validate(url, request.POST, signature):
                    return HttpResponseForbidden()
            if request.method == 'GET':
                if not validator.validate(url, request.GET, signature):
                    return HttpResponseForbidden()

        # If the user requesting service is blacklisted, reject their
        # request.
        if blacklist:
            blacklisted_resp = get_blacklisted_response(request)
            if blacklisted_resp:
                return blacklisted_resp

        # Run the wrapped view, and capture the data returned.
        response = f(request_or_self, *args, **kwargs)

        # If the view returns a string (or a ``twilio.Verb`` object), we'll
        # assume it is TWiML and pass it back with the appropriate
        # mimetype. We won't check the XML data because that would be too time
        # consuming for every request. Instead, we'll let the errors pass
        # through to be dealt with by the developer.
        if isinstance(response, str):
            return HttpResponse(response, content_type='application/xml')
        elif isinstance(response, Verb):
            return HttpResponse(str(response), content_type='application/xml')
        else:
            return response
    return decorator
