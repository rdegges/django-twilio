# -*- coding: utf-8 -*-
import django
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest

if django.get_version() > "3.0.0":
    from django.core.handlers.asgi import ASGIRequest


from .exceptions import NotDjangoRequestException


class TwilioRequest(object):
    '''
    Primarily a collection of key/values from a Twilio HTTP request.
    Also has some additional attributes to support development with the
    Twilio API
    '''

    def __init__(self, parameters):
        self._build_params(parameters)

    def _build_params(self, parameters):
        '''
        Build out the Twilio key/values from the parameters into attributes
        on this class.
        '''
        for key, value in parameters.items():
            if key == 'From':
                setattr(self, 'from_', value)
            else:
                setattr(self, key.lower(), value)
        if getattr(self, 'callsid', False):
            self.type = 'voice'
        elif getattr(self, 'messagesid', False):
            self.type = 'message'
        else:
            self.type = 'unknown'


def decompose(request):
    '''
    Decompose takes a Django HttpRequest object and tries to collect the
    Twilio-specific POST parameters and return them in a TwilioRequest object.
    '''
    request_types = [HttpRequest, WSGIRequest]
    try:
        request_types.append(ASGIRequest)
    except NameError:
        pass
    if type(request) not in request_types:
        raise NotDjangoRequestException(
            'The request parameter is not a Django HttpRequest object')
    if request.method == 'POST':
        return TwilioRequest(request.POST.dict())
    if request.method == 'GET':
        return TwilioRequest(request.GET.dict())
