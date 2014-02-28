from django.test import TestCase
from django.contrib.auth.models import User

from twilio.rest import TwilioRestClient

from django_twilio.client import twilio_client
from django_twilio.models import Credential
from django_twilio import settings
from django_twilio.utils import discover_twilio_creds


class TwilioClientTestCase(TestCase):

    def test_twilio_client_exists(self):
        self.assertIsInstance(twilio_client, TwilioRestClient)

    def test_twilio_client_sets_creds(self):
        self.assertEqual(
            twilio_client.auth,
            (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN))

    def test_twilio_client_with_creds_model(self):
        self.user = User.objects.create(username='test', password='pass')
        self.creds = Credential.objects.create(
            name='Test Creds',
            account_sid='AAA',
            auth_token='BBB',
            user=self.user,
        )

        deets = discover_twilio_creds(user=self.user)

        self.assertEquals(deets[0], self.creds.account_sid)
        self.assertEquals(deets[1], self.creds.auth_token)
