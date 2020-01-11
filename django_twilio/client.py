# -*- coding: utf-8 -*-

"""
Twilio REST client helpers.
"""

from twilio.rest import Client

from .settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


twilio_client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)
