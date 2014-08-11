# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.http import HttpResponse
from django.test import Client, TestCase
from django.test.utils import override_settings

from twilio import twiml
from django_dynamic_fixture import G

from django_twilio.models import Caller

from .views import (response_view, str_view, bytes_view, verb_view,
                    BytesView, StrView, VerbView, ResponseView)
from .utils import TwilioRequestFactory


class TwilioViewTestCase(TestCase):

    urls = 'test_project.test_app.urls'

    def setUp(self):

        self.regular_caller = G(Caller, phone_number='+12222222222', blacklisted=False)
        self.blocked_caller = G(Caller, phone_number='+13333333333', blacklisted=True)

        self.factory = TwilioRequestFactory(
            token=settings.TWILIO_AUTH_TOKEN,
            enforce_csrf_checks=True,
        )

        # Test URIs.
        self.str_uri = '/test_app/decorators/str_view/'
        self.str_class_uri = '/test_app/decorators/str_class_view/'
        self.bytes_uri = '/test_app/decorators/bytes_view/'
        self.bytes_class_uri = '/test_app/decorators/bytes_class_view/'
        self.verb_uri = '/test_app/decorators/verb_view/'
        self.verb_class_uri = 'test_app/decorators/verb_class_view/'
        self.response_uri = '/test_app/decorators/response_view/'
        self.response_class_uri = 'test_app/decorators/response_class_view/'

    def test_requires_get_or_post(self):
        client = Client(enforce_csrf_checks=True)
        with override_settings(DEBUG=False):
            self.assertEquals(client.get(self.str_uri).status_code, 403)
            self.assertEquals(client.post(self.str_uri).status_code, 403)
            self.assertEquals(client.head(self.str_uri).status_code, 405)
            self.assertEquals(client.options(self.str_uri).status_code, 405)
            self.assertEquals(client.put(self.str_uri).status_code, 405)
            self.assertEquals(client.delete(self.str_uri).status_code, 405)

            self.assertEquals(client.get(self.str_class_uri).status_code, 403)
            self.assertEquals(client.post(self.str_class_uri).status_code, 403)
            self.assertEquals(client.head(self.str_class_uri).status_code, 405)
            self.assertEquals(client.put(self.str_class_uri).status_code, 405)
            self.assertEquals(client.delete(self.str_class_uri).status_code, 405)

        with override_settings(DEBUG=True):
            self.assertEquals(client.get(self.str_uri).status_code, 200)
            self.assertEquals(client.post(self.str_uri).status_code, 200)
            self.assertEquals(client.head(self.str_uri).status_code, 200)
            self.assertEquals(client.options(self.str_uri).status_code, 200)
            self.assertEquals(client.put(self.str_uri).status_code, 200)
            self.assertEquals(client.delete(self.str_uri).status_code, 200)

            self.assertEquals(client.get(self.str_class_uri).status_code, 200)
            self.assertEquals(client.post(self.str_class_uri).status_code, 200)
            self.assertEquals(client.head(self.str_class_uri).status_code, 200)

    def test_allows_post(self):
        request = self.factory.post(self.str_uri)
        self.assertEquals(str_view(request).status_code, 200)

    def test_class_view_allows_post(self):
        request = self.factory.post(self.str_class_uri)
        self.assertEquals(StrView.as_view()(request).status_code, 200)

    def test_decorator_preserves_metadata(self):
        self.assertEqual(str_view.__name__, 'str_view')

    def test_class_decorator_preserves_metadata(self):
        self.assertEqual(StrView.dispatch.__name__, 'dispatch')

    @override_settings(TWILIO_ACCOUNT_SID=None)
    @override_settings(TWILIO_AUTH_TOKEN=None)
    def test_missing_settings_return_forbidden(self):
        with override_settings(DEBUG=False):
            self.assertEquals(self.client.post(self.str_uri).status_code, 403)
            self.assertEqual(self.client.post(self.str_class_uri).status_code, 403)
        with override_settings(DEBUG=True):
            self.assertEquals(self.client.post(self.str_uri).status_code, 200)
            self.assertEquals(self.client.post(self.str_class_uri).status_code, 200)

    def test_missing_signature_returns_forbidden(self):
        with override_settings(DEBUG=False):
            self.assertEquals(self.client.post(self.str_uri).status_code, 403)
            self.assertEquals(self.client.post(self.str_class_uri).status_code, 403)
        with override_settings(DEBUG=True):
            self.assertEquals(self.client.post(self.str_uri).status_code, 200)
            self.assertEquals(self.client.post(self.str_class_uri).status_code, 200)

    def test_incorrect_signature_returns_forbidden(self):
        with override_settings(DEBUG=False):
            request = self.factory.post(
                self.str_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(str_view(request).status_code, 403)
        with override_settings(DEBUG=True):
            self.assertEquals(str_view(request).status_code, 200)

    def test_incorrect_signature_returns_forbidden_class_view(self):
        with override_settings(DEBUG=False):
            request = self.factory.post(
                self.str_class_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(StrView.as_view()(request).status_code, 403)
        with override_settings(DEBUG=True):
            self.assertEquals(StrView.as_view()(request).status_code, 200)

    def test_no_from_field(self):
        request = self.factory.post(self.str_uri)
        self.assertEquals(str_view(request).status_code, 200)

    def test_no_form_field_class_view(self):
        request = self.factory.post(self.str_class_uri)
        self.assertEquals(StrView.as_view()(request).status_code, 200)

    def test_from_field_no_caller(self):
        request = self.factory.post(self.str_uri, {'From': '+12222222222'})
        self.assertEquals(str_view(request).status_code, 200)

    def tst_form_field_no_caller_class_view(self):
        request = self.factory.post(self.str_class_uri, {'From': '+12222222222'})
        self.assertEquals(StrView.as_view()(request).status_code, 200)

    def test_blacklist_works(self):
        with override_settings(DEBUG=False):
            request = self.factory.post(self.str_uri, {'From': '+13333333333'})
            response = str_view(request)
            r = twiml.Response()
            r.reject()
            self.assertEquals(
                response.content,
                str(r).encode('utf-8'),
            )
        with override_settings(DEBUG=True):
            request = self.factory.post(self.str_uri, {'From': '+13333333333'})
            response = str_view(request)
            r = twiml.Response()
            r.reject()
            self.assertEquals(
                response.content,
                str(r).encode('utf-8'),
            )

    def test_black_list_works_class_view(self):
        with override_settings(DEBUG=False):
            request = self.factory.post(self.str_class_uri, {'From': '+13333333333'})
            response = StrView.as_view()(request)
            r = twiml.Response()
            r.reject()
            self.assertEquals(
                response.content,
                str(r).encode('utf-8'),
            )
        with override_settings(DEBUG=True):
            request = self.factory.post(self.str_class_uri, {'From': '+13333333333'})
            response = StrView.as_view()(request)
            r = twiml.Response()
            r.reject()
            self.assertEquals(
                response.content,
                str(r).encode('utf-8'),
            )

    def test_decorator_modifies_str(self):
        request = self.factory.post(self.str_uri)
        self.assertIsInstance(str_view(request), HttpResponse)

    def test_decorator_modifies_str_class_view(self):
        request = self.factory.post(self.str_class_uri)
        self.assertIsInstance(StrView.as_view()(request), HttpResponse)

    def test_decorator_modifies_bytes(self):
        request = self.factory.post(self.bytes_uri)
        self.assertIsInstance(bytes_view(request), HttpResponse)

    def test_decorator_modifies_bytes_class_view(self):
        request = self.factory.post(self.bytes_class_uri)
        self.assertIsInstance(BytesView.as_view()(request), HttpResponse)

    def test_decorator_modifies_verb(self):
        request = self.factory.post(self.verb_uri)
        self.assertIsInstance(verb_view(request), HttpResponse)

    def test_decorator_modifies_verb_class_view(self):
        request = self.factory.post(self.verb_class_uri)
        self.assertIsInstance(VerbView.as_view()(request), HttpResponse)

    def test_decorator_preserves_http_response(self):
        request = self.factory.post(self.response_uri)
        self.assertIsInstance(response_view(request), HttpResponse)

    def test_decorator_preserves_http_response_class_view(self):
        request = self.factory.post(self.response_class_uri)
        self.assertIsInstance(ResponseView.as_view()(request), HttpResponse)

    def test_override_forgery_protection_off_debug_off(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=False, DEBUG=False):
            request = self.factory.post(
                self.str_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(str_view(request).status_code, 200)

    def test_override_forgery_protection_off_debug_off_class_view(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=False, DEBUG=False):
            request = self.factory.post(
                self.str_class_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(StrView.as_view()(request).status_code, 200)

    def test_override_forgery_protection_off_debug_on(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=False, DEBUG=True):
            request = self.factory.post(
                self.str_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(str_view(request).status_code, 200)

    def test_override_forgery_protection_off_debug_on_class_view(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=False, DEBUG=True):
            request = self.factory.post(
                self.str_class_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(StrView.as_view()(request).status_code, 200)

    def test_override_forgery_protection_on_debug_off(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=True, DEBUG=False):
            request = self.factory.post(
                self.str_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(str_view(request).status_code, 403)

    def test_override_forgery_protection_on_debug_off_class_view(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=True, DEBUG=False):
            request = self.factory.post(
                self.str_class_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(StrView.as_view()(request).status_code, 403)

    def test_override_forgery_protection_on_debug_on(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=True, DEBUG=True):
            request = self.factory.post(
                self.str_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(str_view(request).status_code, 403)

    def test_override_forgery_protection_on_debug_on_class_view(self):
        with override_settings(DJANGO_TWILIO_FORGERY_PROTECTION=True, DEBUG=True):
            request = self.factory.post(
                self.str_class_uri,
                HTTP_X_TWILIO_SIGNATURE='fake_signature',
            )
            self.assertEquals(StrView.as_view()(request).status_code, 403)
