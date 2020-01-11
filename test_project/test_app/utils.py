# -*- coding: utf-8 -*-

from urllib.parse import urljoin

from twilio.request_validator import RequestValidator

from django.test import RequestFactory


class TwilioRequestFactory(RequestFactory):

    def __init__(self, token, **defaults):
        super(TwilioRequestFactory, self).__init__(**defaults)
        self.base_url = 'http://testserver/'
        self.twilio_auth_token = token

    def _compute_signature(self, path, params):
        return RequestValidator(
            self.twilio_auth_token
        ).compute_signature(urljoin(self.base_url, path), params=params)

    def get(self, path, data={}, **extra):
        if 'HTTP_X_TWILIO_SIGNATURE' not in extra:
            extra.update({'HTTP_X_TWILIO_SIGNATURE': self._compute_signature(path, params=data)})
        return super(TwilioRequestFactory, self).get(path, data, **extra)

    def post(self, path, data={}, content_type=None, **extra):
        if 'HTTP_X_TWILIO_SIGNATURE' not in extra:
            extra.update({'HTTP_X_TWILIO_SIGNATURE': self._compute_signature(path, params=data)})
        if content_type is None:
            return super(TwilioRequestFactory, self).post(path, data, **extra)
        else:
            return super(TwilioRequestFactory, self).post(path, data, content_type, **extra)
