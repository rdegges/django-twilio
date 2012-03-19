from types import MethodType

from django.test import TestCase

from django_twilio.models import Caller


class CallerTestCase(TestCase):
    """Run tests against the :class:`django_twilio.models.Caller` model ."""

    def setUp(self):
        self.caller = Caller.objects.create(phone_number='+12223334444')

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
