# -*- coding: utf-8 -*-

from types import MethodType

from django.test import TestCase
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from django_twilio.models import Caller, Credential


class CallerTestCase(TestCase):
    """
    Run tests against the :class:`django_twilio.models.Caller` model.
    """

    def setUp(self):
        self.caller = G(
            Caller,
            phone_number='+15005550000',
            blacklisted=False,
        )

    def test_has_str_method(self):
        self.assertIsInstance(self.caller.__str__, MethodType)

    def test_str_returns_a_string(self):
        self.assertIsInstance(self.caller.__str__(), str)

    def test_str_doesnt_contain_blacklisted(self):
        self.assertNotIn('blacklisted', self.caller.__str__())

    def test_unicode_contains_blacklisted(self):
        self.caller.blacklisted = True
        self.caller.save()
        self.assertIn('blacklisted', self.caller.__str__())


class CredentialTests(TestCase):

    def setUp(self):
        self.user = G(User, username='test', password='pass')
        self.credentials = G(
            Credential,
            name='Test Credentials',
            account_sid='XXX',
            auth_token='YYY',
            user=self.user,
        )

    def test_str(self):
        """
        Assert that str renders how we'd like it too
        """
        self.assertEqual(
            self.credentials.__str__(),
            'Test Credentials - XXX',
        )

    def test_credentials_fields(self):
        """
        Assert the fields are working correctly
        """
        self.assertEqual(self.credentials.name, 'Test Credentials')
        self.assertEqual(self.credentials.account_sid, 'XXX')
        self.assertEqual(self.credentials.auth_token, 'YYY')
        self.assertEqual(self.credentials.user, self.user)
