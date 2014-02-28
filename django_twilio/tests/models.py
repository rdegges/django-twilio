from types import MethodType

from django.test import TestCase
from django.contrib.auth.models import User
from django_twilio.models import Caller, Credential


class CallerTestCase(TestCase):
    """Run tests against the :class:`django_twilio.models.Caller` model ."""

    def setUp(self):
        self.caller = Caller.objects.create(
            phone_number='12223334444', blacklisted=False)

    def test_has_unicode(self):
        self.assertTrue(isinstance(self.caller.__unicode__, MethodType))

    def test_unicode_returns_str(self):
        self.assertTrue(isinstance(self.caller.__unicode__(), str))

    def test_unicode_doesnt_contain_blacklisted(self):
        self.assertFalse('blacklisted' in self.caller.__unicode__())

    def test_unicode_contains_blacklisted(self):
        self.caller.blacklisted = True
        self.caller.save()
        self.assertTrue('blacklisted' in self.caller.__unicode__())

    def tearDown(self):
        self.caller.delete()


class CredentialTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='pass')
        self.creds = Credential.objects.create(
            name='Test Creds',
            account_sid='XXX',
            auth_token='YYY',
            user=self.user,
        )

    def test_unicode(self):
        ''' Assert that unicode renders how we'd like it too '''
        self.assertEquals(self.creds.__unicode__(), 'Test Creds - XXX')

    def test_credentials_fields(self):
        ''' Assert the fields are working correctly '''
        self.assertEquals(self.creds.name, 'Test Creds')
        self.assertEquals(self.creds.account_sid, 'XXX')
        self.assertEquals(self.creds.auth_token, 'YYY')
        self.assertEquals(self.creds.user, self.user)
