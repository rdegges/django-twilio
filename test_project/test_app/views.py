# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase
from twilio.twiml.voice_response import VoiceResponse

from django_twilio.decorators import twilio_view
from django.views.generic import View
from django.utils.decorators import method_decorator

from django_twilio.views import (
    conference, dial, gather, play, record, say, sms, message
    )

from .utils import TwilioRequestFactory


@twilio_view
def response_view(request):
    """
    A simple test view that returns a HttpResponse object.
    """
    return HttpResponse(
        '<Response><Message>Hello from Django</Message></Response>',
        content_type='text/xml',
    )


class ResponseView(View):

    @method_decorator(twilio_view)
    def dispatch(self, request, *args, **kwargs):
        return super(ResponseView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse(
            '<Response><Message>Hello from Django</Message></Response>',
            content_type='text/xml',
        )

    def post(self, request):
        return HttpResponse(
           '<Response><Message>Hello from Django</Message></Response>',
            content_type='text/xml',
        )


@twilio_view
def str_view(request):
    """
    A simple test view that returns a string.
    """
    return '<Response><Message>Hi!</Message></Response>'


class StrView(View):

    @method_decorator(twilio_view)
    def dispatch(self, request, *args, **kwargs):
        return super(StrView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return '<Response><Message>Hi!</Message></Response>'

    def post(self, request):
        return '<Response><Message>Hi!</Message></Response>'


@twilio_view
def bytes_view(request):
    """
    A simple test view that returns ASCII bytes.
    """
    return b'<Response><Message>Hi!</Message></Response>'


class BytesView(View):

    @method_decorator(twilio_view)
    def dispatch(self, request, *args, **kwargs):
        return super(BytesView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return b'<Response><Message>Hi!</Message></Response>'

    def post(self, request):
        return b'<Response><Message>Hi!</Message></Response>'


@twilio_view
def verb_view(request):
    """
    A simple test view that returns a ``twilio.Verb`` object.
    """
    r = VoiceResponse()
    r.reject()
    return r


class VerbView(View):

    @method_decorator(twilio_view)
    def dispatch(self, request, *args, **kwargs):
        return super(VerbView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        r = VoiceResponse()
        r.reject()
        return r

    def post(self, request):
        r = VoiceResponse()
        r.reject()
        return r


class SayTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.say_uri = '/test_app/views/say/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)
        self.request = self.factory.post(self.say_uri)

    def test_say_no_text(self):
        self.assertRaises(TypeError, say, self.request)

    def test_say_with_text(self):
        self.assertEqual(
            say(self.request, text='hi').status_code,
            200
        )


class PlayTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.play_uri = '/test_app/views/play/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)

    def test_play_no_url(self):
        request = self.factory.post(self.play_uri)
        self.assertRaises(TypeError, play, request)

    def test_play_with_url(self):
        request = self.factory.post(self.play_uri)
        self.assertEqual(
            play(request, url='http://b.com/b.wav').status_code,
            200,
        )


class GatherTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.gather_uri = '/test_app/views/gather/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)

    def test_gather(self):
        request = self.factory.post(self.gather_uri)
        self.assertEqual(
            gather(request).status_code,
            200,
        )


class RecordTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.record_uri = '/test_app/views/record/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)

    def test_record(self):
        request = self.factory.post(self.record_uri)
        self.assertEqual(
            record(request).status_code,
            200,
        )


class SmsTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.sms_uri = '/test_app/views/sms/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)

    def test_sms_no_message(self):
        request = self.factory.post(self.sms_uri)
        self.assertRaises(TypeError, sms, request)

    def test_sms_with_message(self):
        request = self.factory.post(self.sms_uri)
        self.assertEqual(
            sms(request, message='test').status_code,
            200,
        )

class MessageTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.message_uri = '/test_app/views/message/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)

    def test_message_no_message(self):
        request = self.factory.post(self.message_uri)
        self.assertRaises(TypeError, message, request)

    def test_message_with_media(self):
        request = self.factory.post(self.message_uri)
        self.assertEqual(
            message(
                request,
                message='test',
                media='http://i.imgur.com/Qa8GVPU.gif'
            ).status_code,
            200,
        )


class DialTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.dial_uri = '/test_app/views/dial/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)

    def test_dial_no_number(self):
        request = self.factory.post(self.dial_uri)
        self.assertRaises(TypeError, dial, request)

    def test_dial_with_number(self):
        request = self.factory.post(self.dial_uri)
        self.assertEqual(
            dial(request, number='+18182223333').status_code,
            200,
        )


class ConferenceTestCase(TestCase):

    def setUp(self):

        # Test URI
        self.conf_uri = '/test_app/views/conference/'

        self.factory = TwilioRequestFactory(token=settings.TWILIO_AUTH_TOKEN)

    def test_conference_no_name(self):
        request = self.factory.post(self.conf_uri)
        self.assertRaises(TypeError, conference, request)

    def test_conference_with_name(self):
        request = self.factory.post(self.conf_uri)
        self.assertEqual(
            conference(request, name='a').status_code,
            200,
        )
