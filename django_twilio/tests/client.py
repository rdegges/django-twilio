from django.test import TestCase

from twilio.rest import TwilioRestClient

from django_twilio.client import twilio_client
from django_twilio import settings


class TwilioClientTestCase(TestCase):

    def test_twilio_client_exists(self):
        self.assertIsInstance(twilio_client, TwilioRestClient)

    def test_twilio_client_sets_creds(self):
        self.assertEqual(
            twilio_client.auth,
            (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN))
