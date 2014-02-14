"""django_twilio specific settings."""


from django.conf import settings
import os

TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', '')

if not TWILIO_ACCOUNT_SID:
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID'] \
        if 'TWILIO_ACCOUNT_SID' in os.environ else ''
if not TWILIO_AUTH_TOKEN:
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_ACCOUNT_SID'] \
        if 'TWILIO_ACCOUNT_SID' in os.environ else ''
