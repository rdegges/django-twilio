from twilio.twiml import Response
from django_twilio.decorators import twilio_view


@twilio_view
def say(request, text, voice=None, language=None, loop=None):
    """Use twilio's text-to-speech engine to read off a message to the caller.
    Full documentation available on twilio's website:
    http://www.twilio.com/docs/api/twiml/say.

    :param str text: The text to read to the caller. Limited to 4KB.

    :param str voice: Which voice should Twilio use when reading the text?
        Available options are 'man' or 'woman'. Defaults to 'man'.

    :param str language: Twilio currently supports languages 'en' (English),
        'es' (Spanish), 'fr' (French), and 'de' (German). Defaults to 'en'.

    :param int loop: How many times should Twilio repeat the text? Defaults to
        1. Specifying 0 will make Twilio repeat the text until the caller hangs
        up.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^say/$', 'django_twilio.views.say', {'text': 'hello, world!'})
            # ...
        )
    """
    r = Response()
    r.say(text, voice=voice, language=language, loop=loop)
    return r


@twilio_view
def play(request, url, loop=None):
    """Play an audio file to the caller. Full documentation available on
    twilio's website: http://www.twilio.com/docs/api/twiml/play.

    :param str url: The URL of an audio file for Twilio to play to the caller.

    :param int loop: How many times should Twilio play the file? Deafults to 1.
        Speciying 0 will make Twilio repeat the recording until the caller hangs
        up.

    Twilio supports the following audio MIME types for audio files:

    +--------------+-------------------------------+
    | MIME Type    | Description                   |
    +==============+===============================+
    | audio/mpeg   | mpeg layer 3 audio            |
    +--------------+-------------------------------+
    | audio/wav    | wav format audio              |
    +--------------+-------------------------------+
    | audio/wave   | wav format audio              |
    +--------------+-------------------------------+
    | audio/x-wav  | wav format audio              |
    +--------------+-------------------------------+
    | audio/aiff   | audio interchange file format |
    +--------------+-------------------------------+
    | audio/x-aifc | audio interchange file format |
    +--------------+-------------------------------+
    | audio/x-aiff | audio interchange file format |
    +--------------+-------------------------------+
    | audio/x-gsm  | GSM audio format              |
    +--------------+-------------------------------+
    | audio/gsm    | GSM audio format              |
    +--------------+-------------------------------+
    | audio/ulaw   | u-law audio format            |
    +--------------+-------------------------------+

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
    r = Response()
    r.play(url, loop=loop)
    return r


@twilio_view
def gather(request, action=None, method=None, num_digits=None, timeout=None,
        finish_on_key=None):
    """See: http://www.twilio.com/docs/api/twiml/gather.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^gather/$', 'django_twilio.views.gather'),
            # ...
        )
    """
    r = Response()
    r.gather(action=action, method=method, numDigits=num_digits,
        timeout=timeout, finishOnKey=finish_on_key)
    return r


@twilio_view
def record(request, action=None, method=None, timeout=None, finish_on_key=None,
        max_length=None, transcribe=None, transcribe_callback=None,
        play_beep=None):
    """See: http://www.twilio.com/docs/api/twiml/record.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^record/$', 'django_twilio.views.record'),
            # ...
        )
    """
    r = Response()
    r.record(action=action, method=method, timeout=timeout,
        finishOnKey=finish_on_key, maxLength=max_length,
        transcribe=transcribe, transcribeCallback=transcribe_callback,
        playBeep=play_beep)
    return r


@twilio_view
def sms(request, message, to=None, sender=None, action=None, method=None,
        status_callback=None):
    """See: http://www.twilio.com/docs/api/twiml/sms.

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
    r = Response()
    r.sms(msg=message, to=to, sender=sender, method=method, action=action,
            statusCallback=status_callback)
    return r


@twilio_view
def dial(request, number, action=None, method=None, timeout=None,
        hangup_on_star=None, time_limit=None, caller_id=None):
    """See: http://www.twilio.com/docs/api/twiml/dial.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^dial/?(P<number>\\w+)/$', 'django_twilio.views.dial'),
            # ...
        )
    """
    r = Response()
    r.dial(number=number, action=action, method=method, timeout=timeout,
            hangupOnStar=hangup_on_star, timeLimit=time_limit,
            callerId=caller_id)
    return r


@twilio_view
def conference(request, name, muted=None, beep=None,
        start_conference_on_enter=None, end_conference_on_exit=None,
        wait_url=None, wait_method=None, max_participants=None):
    """See: http://www.twilio.com/docs/api/twiml/conference.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^conference/?(P<name>\\w+)/$', 'django_twilio.views.conference',
                    {'max_participants': 10}),
            # ...
        )
    """
    r = Response()
    r.dial().conference(
        name = name,
        muted = muted,
        beep = beep,
        startConferenceOnEnter = start_conference_on_enter,
        endConferenceOnExit = end_conference_on_exit,
        waitUrl = wait_url,
        waitMethod = wait_method,
    )
    return r
