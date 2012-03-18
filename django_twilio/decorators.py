"""Useful decorators."""


from functools import wraps

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseForbidden

from twilio.twiml import Response, Verb
from twilio.util import RequestValidator

from django_twilio import conf
from django_twilio.models import Caller


def get_blacklisted_response(request):
    """Helper function to reject blacklisted callers.
    """
    try:
        caller = Caller.objects.get(phone_number=request.POST['From'])
        if caller.blacklisted:
            r = Response()
            r.reject()
            return HttpResponse(str(r), mimetype='application/xml')
    except (KeyError, Caller.DoesNotExist):
        pass
    return None


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
            At this time this ONLY supports XML TwiML since the Twilio
            library only supports XML rendering at the moment. In future
            releases this may be changed to support JSON (and other formats) as
            well.

    Usage::

        from twilio.twiml import Response

        @twilio_view
        def my_view(request):
            r = Response()
            r.sms('Thanks for the SMS message!')
            return r
    """
    @csrf_exempt
    @wraps(f)
    def decorator(request, *args, **kwargs):
        # Attempt to gather all required information to allow us to check the
        # incoming HTTP request for forgery. If any of this information is not
        # available, then we'll throw a HTTP 403 error (forbidden).
        #
        # The required fields to check for forged requests are:
        #
        #   1. ``TWILIO_ACCOUNT_SID`` (set in the site's settings module).
        #   2. ``TWILIO_AUTH_TOKEN`` (set in the site's settings module).
        #   3. The full URI of the request, eg: 'http://mysite.com/test/view/'.
        #      This may not necessarily be available if this view is being
        #      called via a unit testing library, or in certain localized
        #      environments.
        #   4. A special HTTP header, ``HTTP_X_TWILIO_SIGNATURE`` which
        #      contains a hash that we'll use to check for forged requests.
        if not settings.DEBUG:
            # Ensure the request method is POST
            response = require_POST(f)(request, *args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            
            # Validate the request
            try:
                validator = RequestValidator(conf.TWILIO_AUTH_TOKEN)
                url = request.build_absolute_uri()
                signature = request.META['HTTP_X_TWILIO_SIGNATURE']
            except (AttributeError, KeyError):
                return HttpResponseForbidden()
    
            # Now that we have all the required information to perform forgery
            # checks, we'll actually do the forgery check.
            if not validator.validate(url, request.POST, signature):
                return HttpResponseForbidden()
    
            # If the caller requesting service is blacklisted, reject their
            # request.
            blacklisted_resp = get_blacklisted_response(request)
            if blacklisted_resp is not None:
                return blacklisted_resp
    
            # Run the wrapped view, and capture the data returned.
            response = f(request, *args, **kwargs)
        else:
            # If the caller requesting service is blacklisted, reject their
            # request.
            blacklisted_resp = get_blacklisted_response(request)
            if blacklisted_resp is not None:
                return blacklisted_resp
            
            # Run the wrapped view, and capture the data returned.
            response = f(request, *args, **kwargs)

        # If the view returns a string (or a ``twilio.Verb`` object), we'll
        # assume it is XML TwilML data and pass it back with the appropriate
        # mimetype. We won't check the XML data because that would be too time
        # consuming for every request. Instead, we'll let the errors pass
        # through to be dealt with by the developer.
        if isinstance(response, str):
            return HttpResponse(response, mimetype='application/xml')
        elif isinstance(response, Verb):
            return HttpResponse(str(response), mimetype='application/xml')
        else:
            return response
    return decorator
