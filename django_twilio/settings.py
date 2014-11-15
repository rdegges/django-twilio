# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
django_twilio specific settings.
"""

import os

from django.conf import settings

def discover_twilio_credentials(user=None):
    """ Due to the multiple ways of providing SID / AUTH tokens through
        this package, this function will search in the various places that
        credentials might be stored.

        The order this is done in is:

        1. If a User is passed: the keys linked to the
           user model from the Credentials model in the database.
        2. Environment variables
        3. django.conf settings

        We recommend using environment variables were possible; it is the
        most secure option
    """

    SID = 'TWILIO_ACCOUNT_SID'
    AUTH = 'TWILIO_AUTH_TOKEN'

    if user:
        return user.account_sid, user.auth_token

    if SID in os.environ and AUTH in os.environ:
        return os.environ[SID], os.environ[AUTH]

    if hasattr(settings, SID) and hasattr(settings, AUTH):
        return settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN

    raise AttributeError(
        "Could not find {sid} or {auth} in environment variables, "
        "User credentials, or django project settings.".format(
            sid=SID,
            auth=AUTH,
        )
    )

TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN = discover_twilio_credentials()
