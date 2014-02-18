# -*- coding: utf-8 -*-

"""Twilio REST client helpers."""
from django_twilio import settings

from twilio.rest import TwilioRestClient

twilio_client = TwilioRestClient(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN, version='2010-04-01')
