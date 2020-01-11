# -*- coding: utf-8 -*-

from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.twiml.messaging_response import MessagingResponse

from .decorators import twilio_view


@twilio_view
def say(request, text, voice=None, language=None, loop=None):
    """
See: http://www.twilio.com/docs/api/twiml/say.

Usage::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^say/$', 'django_twilio.views.say', {'text': 'hello, world!'})
        # ...
    )
    """
    r = VoiceResponse()
    r.say(text, voice=voice, language=language, loop=loop)
    return r


@twilio_view
def play(request, url, loop=None):
    """
    See: http://www.twilio.com/docs/api/twiml/play.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^play/$', 'django_twilio.views.play', {
                    'url': 'http://blah.com/blah.wav',
            }),
            # ...
        )
    """
    r = VoiceResponse()
    r.play(url, loop=loop)
    return r


@twilio_view
def gather(request, action=None, method='POST', num_digits=None, timeout=None,
           finish_on_key=None):
    """
    See: http://www.twilio.com/docs/api/twiml/gather.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^gather/$', 'django_twilio.views.gather'),
            # ...
        )
    """
    r = VoiceResponse()
    r.gather(action=action, method=method, numDigits=num_digits,
             timeout=timeout, finishOnKey=finish_on_key)
    return r


@twilio_view
def record(request, action=None, method='POST', timeout=None,
           finish_on_key=None, max_length=None, transcribe=None,
           transcribe_callback=None, play_beep=None):
    """
    See: http://www.twilio.com/docs/api/twiml/record.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^record/$', 'django_twilio.views.record'),
            # ...
        )
    """
    r = VoiceResponse()
    r.record(action=action, method=method, timeout=timeout,
             finishOnKey=finish_on_key, maxLength=max_length,
             transcribe=transcribe, transcribeCallback=transcribe_callback,
             playBeep=play_beep)
    return r


@twilio_view
def sms(request, message, to=None, sender=None, action=None, method='POST',
        status_callback=None):
    """
    NOTE: Now deprecated, please use message() instead
    See: http://www.twilio.com/docs/api/twiml/sms

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^sms/$', 'django_twilio.views.sms', {
                'message': 'Hello, world!'
            }),
            # ...
        )
    """
    r = MessagingResponse()
    r.message(message, to=to, sender=sender, method='POST', action=action,
              statusCallback=status_callback)
    return r


@twilio_view
def message(request, message, to=None, sender=None, action=None,
            methods='POST', media=None, status_callback=None):
    """
    See: https://www.twilio.com/docs/api/twiml/sms/message

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^sms/$', 'django_twilio.views.message', {
                'message': 'Hello, world!',
                'media': 'http://fullpath.com/my_image.png'
            }),
            # ...
        )
    """

    r = MessagingResponse()
    r.message(message, to=to, sender=sender, method='POST',
              action=action, statusCallback=status_callback,
              media=media)

    return r


@twilio_view
def dial(request, number, action=None, method='POST', timeout=None,
         hangup_on_star=None, time_limit=None, caller_id=None):
    """
    See: http://www.twilio.com/docs/api/twiml/dial.
    """
    # Usage::
    #
    #     # urls.py
    #     urlpatterns = patterns('',
    #         # ...
    #         url(r'^dial/(?P<number>\w+)/$', 'django_twilio.views.dial'),
    #         # ...
    #     )

    r = VoiceResponse()
    r.dial(number=number, action=action, method=method, timeout=timeout,
           hangupOnStar=hangup_on_star, timeLimit=time_limit,
           callerId=caller_id)
    return r


@twilio_view
def conference(request, name, muted=None, beep=None,
               start_conference_on_enter=None, end_conference_on_exit=None,
               wait_url=None, wait_method='POST', max_participants=None):
    """
    See: http://www.twilio.com/docs/api/twiml/conference.
    """
    # Usage::
    #
    #     # urls.py
    #     urlpatterns = patterns('',
    #         # ...
    #         url(r'^conference/(?P<name>\w+)/$',
    #             'django_twilio.views.conference',
    #              {'max_participants': 10}
    #         ),
    #         # ...
    #     )
    #
    r = VoiceResponse()
    dial = Dial()
    dial.conference(name=name, muted=muted, beep=beep,
                    startConferenceOnEnter=start_conference_on_enter,
                    endConferenceOnExit=end_conference_on_exit,
                    waitUrl=wait_url, waitMethod=wait_method,
                    )
    r.append(dial)
    return r
