"""Useful utility functions."""


from django.http import HttpResponse
from twilio.twiml import Response

from django_twilio.models import Caller


def get_blacklisted_response(request):
    """Analyze the incoming Twilio request to determine whether or not to
    reject services. We'll only reject services if the user requesting service
    is on our blacklist.

    :param obj request: The Django HttpRequest object to analyze.
    :rtype: HttpResponse.
    :returns: HttpResponse if the user requesting services is blacklisted, None
        otherwise.
    """
    try:
        caller = Caller.objects.get(phone_number=request.REQUEST['From'])
        if caller.blacklisted:
            r = Response()
            r.reject()
            return HttpResponse(str(r), mimetype='application/xml')
    except (KeyError, Caller.DoesNotExist):
        pass

    return None
