# -*- coding: utf-8 -*-
from django.test import TestCase
from django.conf import settings

from .utils import TwilioRequestFactory

from django_twilio.request import decompose, TwilioRequest
from django_twilio.exceptions import NotDjangoRequestException


class TestRequestBase(TestCase):

    def setUp(self):
        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)
        self.call_dict = {
            'CallSid': 'CSXXXX',
            'AccountSid': 'ACXXXX',
            'From': '+44123456789',
            'To': '+1123456789',
            'CallStatus': 'queued',
            'ApiVersion': '1',
            'Direction': 'outbound-api',
            'ForwardedFrom': 'False',
            'CallerName': 'Paul'
        }

        self.message_dict = {
            'MessageSid': 'MSXXXX',
            'SmsSid': 'SSXXXX',
            'AccountSid': 'ACXXXX',
            'From': '+1123456789',
            'To': '+44123456789',
            'Body': 'That\'s is no moon!',
            'NumMedia': '0'
        }


class TestDecompose(TestRequestBase):

    def test_voice_decompose_function(self):
        request = self.factory.post(
            '/test_app/decorators/verb_view/',
            self.call_dict
        )
        response = decompose(request)
        self.assertEqual(response.type, 'voice')
        self.assertEqual(response.accountsid, 'ACXXXX')
        self.assertEqual(response.from_, '+44123456789')

    def test_sms_decompose_function(self):
        request = self.factory.post(
            '/test_app/decorators/verb_view',
            self.message_dict
        )
        response = decompose(request)
        self.assertEqual(response.type, 'message')

    def test_blank_decompose_function(self):
        request = self.factory.post(
            '/test_app/decorators/verb_view',
        )
        response = decompose(request)
        self.assertEqual(response.type, 'unknown')

    def test_blank_get_decompose_function(self):
        request = self.factory.get(
            '/test_app/decorators/verb_view?messageSid=ACXXXX',
        )
        response = decompose(request)
        self.assertEqual(response.type, 'message')

    def test_raises_not_django_request_exception(self):
        request = {}
        self.assertRaises(NotDjangoRequestException, decompose, request)
