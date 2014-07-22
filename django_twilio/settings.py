# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
django_twilio specific settings.
"""

from .utils import discover_twilio_credentials

TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN = discover_twilio_credentials()
