from django.test import TestCase

from twilio.rest import TwilioRestClient

from django_twilio.client import twilio_client
from django_twilio.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


class TwilioClientTestCase(TestCase):

    def test_twilio_client_exists(self):
        self.assertIsInstance(twilio_client, TwilioRestClient)

    def test_twilio_client_sets_creds(self):
        self.assertEqual(twilio_client.auth, (TWILIO_ACCOUNT_SID,
                TWILIO_AUTH_TOKEN))
