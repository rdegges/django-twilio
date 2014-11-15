# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from types import MethodType

from django.test import TestCase
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from django_twilio.models import (
    Caller,
    Credential,
    TwoFactorAuthUser,
    TwoFactorAuthUserManager
)

from mock import Mock


class CallerTestCase(TestCase):
    """
    Run tests against the :class:`django_twilio.models.Caller` model.
    """

    def setUp(self):
        self.caller = G(
            Caller,
            phone_number='12223334444',
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
        self.assertEquals(
            self.credentials.__str__(),
            'Test Credentials - XXX',
        )

    def test_credentials_fields(self):
        """
        Assert the fields are working correctly
        """
        self.assertEquals(self.credentials.name, 'Test Credentials')
        self.assertEquals(self.credentials.account_sid, 'XXX')
        self.assertEquals(self.credentials.auth_token, 'YYY')
        self.assertEquals(self.credentials.user, self.user)


class TwoFactorAuthUserTestCase(TestCase):
    """
    Run tests against the :class:`django_twilio.models.TwoFactorAuthUser` model.
    """

    def setUp(self):
        self.user = G(
            TwoFactorAuthUser,
            username='Paul',
            first_name='Paul',
            second_name='Hallett',
            email='hello@phalt.co',
            phone_number='+12223334444',
        )

    def test_has_str_method(self):
        self.assertIsInstance(self.user.__str__, MethodType)

    def test_str_returns_a_string(self):
        self.assertIsInstance(self.user.__str__(), str)

    def test_get_full_name(self):
        self.assertEquals('Paul Hallett', self.user.get_full_name())

    def test_get_short_name(self):
        self.assertEquals('Paul', self.user.get_short_name())

    def test_has_perm(self):
        # Not yet implemented
        self.assertTrue(self.user.has_perm('test'))

    def test_has_module_perm(self):
        # Not yet implemented
        self.assertTrue(self.user.has_module_perms('test'))

    def test_assertion_errors(self):
        self.manager = TwoFactorAuthUserManager()
        self.assertRaises(
            ValueError,
            self.manager.create_user,username=None,
            first_name='Paul',
            second_name='Hallett',
            email='hello@phalt.co',
            phone_number='+12223334444')
        self.assertRaises(
            ValueError,
            self.manager.create_user,username='Paul',
            first_name=None,
            second_name='Hallett',
            email='hello@phalt.co',
            phone_number='+12223334444')
        self.assertRaises(
            ValueError,
            self.manager.create_user,username='Paul',
            first_name='Paul',
            second_name=None,
            email='hello@phalt.co',
            phone_number='+12223334444')
        self.assertRaises(
            ValueError,
            self.manager.create_user,username='Paul',
            first_name='None',
            second_name='Hallett',
            email=None,
            phone_number='+12223334444')
        self.assertRaises(
            ValueError,
            self.manager.create_user,username='Paul',
            first_name='None',
            second_name='Hallett',
            email='hello@phalt.co',
            phone_number=None)

    def test_create_superuser(self):
        self.manager = TwoFactorAuthUserManager()
        self.manager.model = Mock(return_value=self.user)
        result = self.manager.create_superuser(username='Paul',
            first_name='Paul',
            second_name='Hallett',
            email='hello@phalt.co',
            phone_number='+12223334444',
            is_admin=True
        )
        self.assertEquals(result.is_admin, True)

        self.assertTrue(result.is_staff)

    def test_do_two_fa_actions(self):
        self.manager = TwoFactorAuthUserManager()
        result = self.manager.do_two_fa_actions(self.user)
