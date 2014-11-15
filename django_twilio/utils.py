# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
Useful utility functions.
"""

import os
import random

from django.http import HttpResponse
from django.conf import settings

from twilio import twiml

from .models import Caller, Credential


from .settings import discover_twilio_credentials


def discover_twilio_credentials_from_model(user):
    credentials = Credential.objects.filter(user=user.id)
    if credentials.exists():
        credentials = credentials[0]
        return discover_twilio_credentials(credentials)

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
            r = twiml.Response()
            r.reject()
            return HttpResponse(str(r), content_type='application/xml')
    except Exception:
        pass

    return None


# Backwards compatibility for a poorly named function
discover_twilio_creds = discover_twilio_credentials
