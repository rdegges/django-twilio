# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
Twilio REST client helpers.
"""

from twilio.rest import TwilioRestClient

from .settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


twilio_client = TwilioRestClient(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    version='2010-04-01'
)
