# -*- coding: utf-8 -*-
"""Useful utility functions."""

import os

from django.http import HttpResponse
from django.conf import settings

from twilio.twiml import Response

from django_twilio.models import Caller, Credential


def discover_twilio_creds(user=None):
    """ Due to the multiple ways of providing SID / AUTH tokens through
        this package, this function will search in the various places that
        credentials might be stored.

        The order this is done in is:

        1. If a User is passed: the keys linked to the
           user model from the Credentials model in the database.
        2. Environment variables
        3. django.conf settings

        We recommend using enviornment variables were possible, it is the
        most secure option

    """

    SID = 'TWILIO_ACCOUNT_SID'
    AUTH = 'TWILIO_AUTH_TOKEN'

    if user:
        creds = Credential.objects.filter(user=user.id)
        if creds.exists():
            creds = creds[0]
            return (creds.account_sid, creds.auth_token)

    if SID and AUTH in os.environ:
        return (os.environ[SID], os.environ[AUTH])

    return (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


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
            return HttpResponse(str(r), content_type='application/xml')
    except (KeyError, Caller.DoesNotExist):
        pass

    return None
