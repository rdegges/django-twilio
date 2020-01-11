# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

from twilio.rest import Client
from django_dynamic_fixture import G

from django_twilio.client import twilio_client
from django_twilio.models import Credential
from django_twilio.utils import discover_twilio_credentials


class TwilioClientTestCase(TestCase):

    def test_twilio_client_exists(self):
        self.assertIsInstance(twilio_client, Client)

    def test_twilio_client_sets_credentials(self):
        self.assertEqual(
            twilio_client.auth,
            (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        )

    def test_twilio_client_with_credentials_model(self):
        self.user = G(User, username='test', password='pass')
        self.credentials = G(
            Credential,
            name='Test Credentials',
            account_sid='AAA',
            auth_token='BBB',
            user=self.user,
        )

        credentials = discover_twilio_credentials(user=self.user)

        self.assertEqual(credentials[0], self.credentials.account_sid)
        self.assertEqual(credentials[1], self.credentials.auth_token)
