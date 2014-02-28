# -*- coding: utf-8 -*-

"""django_twilio specific settings."""

from .utils import discover_twilio_creds

TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN = discover_twilio_creds()
