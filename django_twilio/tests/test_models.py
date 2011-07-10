from django.test import TestCase

from django_twilio.models import Caller


class CallerTestCase(TestCase):
    """Run tests against the :class:`django_twilio.models.Caller` model ."""

    def setUp(self):
        self.caller = Caller.objects.create(phone_number='+12223334444')

    def test_has_unicode(self):
        self.assertTrue(isinstance(self.caller.__unicode__(), str))

    def tearDown(self):
        self.caller.delete()
