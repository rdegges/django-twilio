# -*- coding: utf-8 -*-

"""
All 2FA management is seperated out here to prevent circular imports with
the standard utils file. (which imports Caller and Credential from models.py)
"""

from __future__ import unicode_literals, absolute_import

import random
from django.conf import settings

from .client import twilio_client

def generate_two_factor_auth_details():
    """
    Generate a set length code and a unique ID for two factor authentication
    """

    code = '{0:04}'.format(random.randint(1, 9999))
    _id = '{0:020}'.format(random.randint(1, 10000000000000000000000))
    return code, _id



def send_two_factor_auth_message(code, to_number, from_number=None):
    """
    Send an SMS message to the number with the code
    """

    message = getattr(
        settings, 'DJANGO_TWILIO_AUTH_MESSAGE',
        'Your authentication code is {{code}}'
    )

    from_ = getattr(
        settings, 'TWILIO_DEFAULT_CALLERID',
        from_number
    )

    if from_ is None:
        raise AttributeError(
        "Could not find TWILIO_DEFAULT_CALLERID variable in settings"
    )

    message = message.replace('{{code}}', code)

    twilio_client.messages.create(
        to=to_number,
        from_=from_,
        body=message
    )
    return True
