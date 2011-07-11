"""Useful decorators."""


from functools import wraps

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseForbidden

from twilio import Response, Utils, Verb

from django_twilio import conf
from django_twilio.models import Caller


def twilio_view(f):
    """This decorator provides several helpful shortcuts for writing twilio
    """
    @csrf_exempt
    @require_POST
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
        try:
            utils = Utils(conf.TWILIO_ACCOUNT_SID, conf.TWILIO_AUTH_TOKEN)
            url = request.build_absolute_uri()
            signature = request.META['HTTP_X_TWILIO_SIGNATURE']
        except (AttributeError, KeyError):
            return HttpResponseForbidden()

        # Now that we have all the required information to perform forgery
        # checks, we'll actually do the forgery check.
        if not utils.validateRequest(url, request.POST, signature):
            return HttpResponseForbidden()

        # If the caller requesting service is blacklisted, reject their
        # request.
        try:
            caller = Caller.objects.get(phone_number=request.POST['From'])
            if caller.blacklisted:
                r = Response()
                r.addReject()
                return HttpResponse(r.__repr__(), mimetype='application/xml')
        except (KeyError, Caller.DoesNotExist):
            pass

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
            return HttpResponse(response.__repr__(), mimetype='application/xml')
        else:
            return response
    return decorator
