# -*- coding: utf-8 -*-

"""Twilio REST client helpers."""
from django_twilio import settings
import os

from twilio.rest import TwilioRestClient

if 'TWILIO_ACCOUNT_SID' and 'TWILIO_AUTH_TOKEN' in os.environ:
    twilio_client = TwilioRestClient(
        os.environ['TWILIO_ACCOUNT_SID'],
        os.environ['TWILIO_AUTH_TOKEN'],
        version='2010-04-01'
    )
else:
    twilio_client = TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN, version='2010-04-01')
