"""Twilio REST client helpers."""


from twilio.rest import TwilioRestClient

from django_twilio import settings


# Create a single global ``twilio_client`` object that already makes use of
# your django-twilio credentials. This allows you to make API calls using the
# Twilio rest API (http://readthedocs.org/docs/twilio-python/en/latest/usage/basics.html#accessing-rest-resources)
# without handling object creation and authentication yourself.
#
# NOTE: I'm explicitly defining the API version here so that if users forcibly
# install a later release of twilio-python that uses a different default API
# version--we'll still be OK.
twilio_client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN, version='2010-04-01')
