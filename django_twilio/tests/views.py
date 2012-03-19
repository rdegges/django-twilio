from hmac import new
from hashlib import sha1
from base64 import encodestring

from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase
from twilio.twiml import Response

from django_twilio import settings
from django_twilio.decorators import twilio_view
from django_twilio.views import conference, dial, gather, play, record, say, \
        sms


@twilio_view
def response_view(request):
    """A simple test view that returns a HttpResponse object."""
    return HttpResponse('<Response><Sms>Hi!</Sms></Response>',
            mimetype='text/xml')


@twilio_view
def str_view(request):
    """A simple test view that returns a string."""
    return '<Response><Sms>Hi!</Sms></Response>'


@twilio_view
def verb_view(request):
    """A simple test view that returns a ``twilio.Verb`` object."""
    r = Response()
    r.reject()
    return r


class SayTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.say_uri = '/tests/views/say/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate Twilio signatures for our test views.
        self.signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/say/' % self.uri, sha1).digest()).strip()

    def test_say_no_text(self):
        request = self.factory.post(self.say_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertRaises(TypeError, say, request)

    def test_say_with_text(self):
        request = self.factory.post(self.say_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertEquals(say(request, text='hi').status_code, 200)


class PlayTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.play_uri = '/tests/views/play/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate twilio signatures for our test views.
        self.signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/play/' % self.uri, sha1).digest()).strip()

    def test_play_no_url(self):
        request = self.factory.post(self.play_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertRaises(TypeError, play, request)

    def test_play_with_url(self):
        request = self.factory.post(self.play_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertEquals(play(request, url='http://b.com/b.wav').status_code, 200)


class GatherTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.gather_uri = '/tests/views/gather/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate twilio signatures for our test views.
        self.signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/gather/' % self.uri, sha1).digest()).strip()

    def test_gather(self):
        request = self.factory.post(self.gather_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertEquals(gather(request).status_code, 200)


class RecordTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.record_uri = '/tests/views/record/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate twilio signatures for our test views.
        self.signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/record/' % self.uri, sha1).digest()).strip()

    def test_record(self):
        request = self.factory.post(self.record_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertEquals(record(request).status_code, 200)


class SmsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.sms_uri = '/tests/views/sms/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate twilio signatures for our test views.
        self.signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/sms/' % self.uri, sha1).digest()).strip()

    def test_sms_no_message(self):
        request = self.factory.post(self.sms_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertRaises(TypeError, sms, request)

    def test_sms_with_message(self):
        request = self.factory.post(self.sms_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertEquals(sms(request, message='test').status_code, 200)


class DialTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.dial_uri = '/tests/views/dial/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate twilio signatures for our test views.
        self.signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/dial/' % self.uri, sha1).digest()).strip()

    def test_dial_no_number(self):
        request = self.factory.post(self.dial_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertRaises(TypeError, dial, request)

    def test_dial_with_number(self):
        request = self.factory.post(self.dial_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertEquals(dial(request, number='+18182223333').status_code, 200)


class ConferenceTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Test URIs.
        self.uri = 'http://testserver/tests/views'
        self.conf_uri = '/tests/views/conference/'

        # Guarantee a value for the required configuration settings after each
        # test case.
        settings.TWILIO_ACCOUNT_SID = 'xxx'
        settings.TWILIO_AUTH_TOKEN = 'xxx'

        # Pre-calculate twilio signatures for our test views.
        self.signature = encodestring(new(settings.TWILIO_AUTH_TOKEN,
                '%s/conference/' % self.uri, sha1).digest()).strip()

    def test_conference_no_name(self):
        request = self.factory.post(self.conf_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertRaises(TypeError, conference, request)

    def test_conference_with_name(self):
        request = self.factory.post(self.conf_uri, HTTP_X_TWILIO_SIGNATURE=self.signature)
        self.assertEquals(conference(request, name='a').status_code, 200)
