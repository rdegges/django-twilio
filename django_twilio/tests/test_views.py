from hmac import new
from hashlib import sha1
from base64 import encodestring

from django.conf import settings
from django.test import Client, RequestFactory, TestCase

from django_twilio.views import conference, say


class ConferenceTestCase(TestCase):
    """Run tests against the ``conference`` view."""

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.conf_uri = '/tests/views/conference/'
        self.say_uri = '/tests/views/say/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate twilio signatures for our test views.
        self.conf_signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/conference/' % self.uri, sha1).digest()).strip()
        self.say_signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/say/' % self.uri, sha1).digest()).strip()

    def test_conference_no_name(self):
        request = self.factory.post(self.conf_uri, HTTP_X_TWILIO_SIGNATURE=self.conf_signature)
        self.assertRaises(TypeError, conference, request)

    def test_conference_with_name(self):
        request = self.factory.post(self.conf_uri, HTTP_X_TWILIO_SIGNATURE=self.conf_signature)
        self.assertEquals(conference(request, name='a').status_code, 200)

    def test_say_no_text(self):
        request = self.factory.post(self.say_uri, HTTP_X_TWILIO_SIGNATURE=self.say_signature)
	self.assertRaises(TypeError, say, request)

    def test_say_with_text(self):
        request = self.factory.post(self.say_uri, HTTP_X_TWILIO_SIGNATURE=self.say_signature)
	self.assertEquals(say(request, text='hi').status_code, 200)
