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
    """Gather touchtone input from a caller. Once the input has been gathered,
    Twilio will (optionally) submit the data to the URL specified in the
    ``action`` parameter via HTTP GET or POST, just like a web browser submits
    data from an HTML form. Full documentation available on twilio's website:
    http://www.twilio.com/docs/api/twiml/gather.

    :param str action: URL that Twilio will GET or POST to after the caller has
        finished entering input. If no action is provided, Twilio will by
        default make a POST request to the current document's URL.

        If ``timeout`` is reached before the caller enters any digits, or if
        the caller enters the ``finish_on_key`` value before entering other
        digits, Twilio will not make a request to the action URL.

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the ``action`` URL:

        +-----------+---------------------------------------------------------+
        | Parameter | Description                                             |
        +===========+=========================================================+
        | Digits    | The digits the caller pressed, excluding the            |
        |           | ``finish_on_key`` digit if used.                        |
        +-----------+---------------------------------------------------------+

    :param str method: Either 'GET' or 'POST'. This tells Twilio whether to
        request the ``action`` URL via HTTP GET or POST. Defaults to 'POST'.

    :param int timeout: Time limit in seconds that Twilio will wait for the
        caller to press another digit before moving on and making a request to
        the ``action`` URL.

    :param str finish_on_key: One value that submits the received data when
        entered. For example, if you set ``finish_on_key`` to '#' and the user
        enters '1234#', Twilio will immediately stop waiting for more input
        when the '#' is received and will submit "Digits=1234" to the
        ``action`` URL. Note that the ``finish_on_key`` value is not sent. The
        allowed values are the digits 0-9, '#' , '*' and the empty string (set
        ``finish_on_key`` to ''). If the empty string is used, Twilio captures
        all input and no key will end input collection. In this case Twilio
        will submit the entered digits to the ``action`` URL only after the
        timeout has been reached. Defaults to '#'.

        .. note::
            The ``finish_on_key`` value **must** be a single character. Multiple
            characters are not allowed.

    :param int num_digits: Maximum number of digits the caller is allowed to
        enter. Once this number of digits is reached, Twilio will automatically
        submit the data to the ``action`` URL. For example, one might set
        ``num_digits`` to 5 and ask the caller to enter a 5 digit zip code.
        When the caller enters the fifth digit of '94117', Twilio will
        immediately submit the data to the ``action`` URL.

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
    """Record a portion of a call, and optionally transcribe the recording.
    Full documentation available on twilio's website:
    http://www.twilio.com/docs/api/twiml/record.

    :param str action: URL that Twilio will GET or POST to after the recording
        has finished. If no action is provided, Twilio will by default make a
        POST to the current document's URL.

        .. note::
            If Twilio receives an empty recording, it will not make a request
            to the ``action`` URL.

        Request Parameters
        ==================

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the ``action`` URL:

        +-------------------+-------------------------------------------------+
        | Parameter         | Description                                     |
        +===================+=================================================+
        | RecordingUrl      | The URL of the recorded audio.                  |
        +-------------------+-------------------------------------------------+
        | RecordingDuration | The time duration of the recorded audio.        |
        +-------------------+-------------------------------------------------+
        | Digits            | The key (if any) pressed to end the recording   |
        |                   | or 'hangup' if the caller hung up.              |
        +-------------------+-------------------------------------------------+
    :param int timeout: Time limit in seconds that Twilio will wait for the
        caller to press another digit before moving on and making a request to
        the ``action`` URL.

    :param str method: Either 'GET' or 'POST'. This tells Twilio whether to
        request the ``action`` URL via HTTP GET or POST. Defaults to 'POST'.

    :param int timeout: The amount of silence (in seconds) after which Twilio
        will automatically end the recording. Defaults to 5.

    :param str finish_on_key: A Set of digits that end the recording when
        entered. For example, if you set ``finish_on_key`` to '#' and the
        caller presses '#', Twilio will immediately stop recording and submit
        'RecordingUrl', 'RecordingDuration', and the '#' as parameters in a
        request to the ``action`` URL. The allowed values are the digits 0-9,
        '#' and '*'. The default is '1234567890*#' (i.e. any key will end the
        recording). Unlike :func:`django_twilio.views.gather`, you may specify
        more than one character as a ``finish_on_key`` value.

    :param int max_length: The maximum length of the recording (in seconds).
        After this time limit has been reached, the recording will automatically
        end. Defaults to 3600 seconds (one hour) for normal recordings, and 120
        seconds (two minutes) for transcribed recordings.

    :param bool transcribe: Enable call transcription of the recording. If
        enabled, Twilio will attempt to convert the audio to human readable
        text. Defaults to False.

        .. note::
            Transcription is a pay feature. If you include a ``transcribe`` or
            ``transcribe_callback`` attribute on your verb your account will be
            charged. See the `pricing page
            <http://www.twilio.com/pricing-signup>`_ for current pricing.

            Additionally, transcription is currently limited to recordings with
            a duration of two minutes or less. If you enable transcription and
            set ``max_length`` > 120 seconds, Twilio will write a warning to
            your debug log rather than transcribing the recording.

    :param str transcribe_callback: The ``transcribe_callback`` attribute is
        used in conjunction with the ``transcribe`` attribute. It allows you to
        specify a URL to which Twilio will make an asynchronous POST request
        when the transcription is complete. This is not a request for TwiML and
        the response will not change call flow, but the request will contain
        the standard TwiML request parameters as well as 'TranscriptionStatus',
        'TranscriptionText', 'TranscriptionUrl' and 'RecordingUrl'. If
        ``transcribe_callback`` is not specified, the completed transcription
        will be stored for you to retrieve later (see the REST API
        Transcriptions section), and Twilio will not asynchronously notify your
        application.

        Request Parameters
        ==================

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the
        ``transcribe_callback`` URL:

        +---------------------+-----------------------------------------------+
        | Parameter           | Description                                   |
        +=====================+===============================================+
        | TranscriptionText   | Contains the text of the transcription.       |
        +---------------------+-----------------------------------------------+
        | TranscriptionStatus | The status of the transcription attempt:      |
        |                     |  either 'completed' or 'failed'.              |
        +---------------------+-----------------------------------------------+
        | TranscriptionUrl    | The URL for the transcription's REST API      |
        |                     |  resource.                                    |
        +---------------------+-----------------------------------------------+
        | RecordingUrl        | The URL for the transcription's source        |
        |                     | recording resource.                           |
        +---------------------+-----------------------------------------------+

    :param bool play_beep: Play a beep before starting the recording. If you set
        this to False, no beep will be played.

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
    """Sends a SMS message to a phone number. Full documentation available on
    twilio's website: http://www.twilio.com/docs/api/twiml/sms.

    :param str message: The message to SMS. Must be less than 140 characters in
        length. If greater than 140 characters, it will not be sent.

    :param str to: Phone number to SMS. Must be in valid `E.164 format
        <http://en.wikipedia.org/wiki/E.164>`_. Defaults to the phone number of
        the caller.

        .. note::
            Sending to short codes is not currently supported.

        .. note::
            Note that if your account is a Free Trial account, the provided
            ``to`` phone number must be validated with Twilio as a valid
            outgoing caller ID. But of course you don't have to specify the
            ``to`` attribute to just send an SMS to the current caller.

    :param str sender: Who to send this message as. Must be a phone number
        you've purchased or ported to Twilio. Defaults to the called party.

    :param str action: URL that Twilio will GET or POST to after sending the SMS
        message with the following parameters: ``SmsStatus`` and ``SmsSid``.
        This is useful if you want notification that the SMS was sent.

        .. note::
            If no ``action`` is specified, then Twilio will simply carry on
            **without** POSTing to the current URL, unlike the other views.

        Request Parameters
        ==================

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the ``action`` URL:

        +-----------+---------------------------------------------------------+
        | Parameter | Description                                             |
        +===========+=========================================================+
        | SmsSid    | The Sid Twilio has assigned for the SMS message.        |
        +-----------+---------------------------------------------------------+
        | SmsStatus | The current status of the SMS message. This is usually  |
        |           | 'sending'. But if you provide an invalid number, this   |
        |           | is 'invalid'.                                           |
        +-----------+---------------------------------------------------------+

    :param str method: Either 'GET' or 'POST'. This tells Twilio whether to
        request the ``action`` URL via HTTP GET or POST. Defaults to 'POST'.

    :param str status_callback: URL for Twilio to post completed SMS status
        information to. This lets you know whether an SMS was successful, or
        failed.

        .. note::
            Twilio always uses POST for this action.

        Request Parameters
        ==================

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the
        ``status_callback`` URL:

        +-----------+---------------------------------------------------------+
        | Parameter | Description                                             |
        +===========+=========================================================+
        | SmsSid    | The Sid for the Sms message.                            |
        +-----------+---------------------------------------------------------+
        | SmsStatus | The current status of the Sms message. Either 'sent' or |
        |           | 'failed'.                                               |
        +-----------+---------------------------------------------------------+

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
    """The ``<Dial>`` verb connects the current caller to an another phone. If
    the called party picks up, the two parties are connected and can
    communicate until one hangs up. If the called party does not pick up, if a
    busy signal is received, or if the number doesn't exist, the dial verb will
    finish.

    When the dialed call ends, Twilio makes a GET or POST request to the
    ``action`` URL if provided. Call flow will continue using the TwiML
    received in response to that request.

    :param str number: Phone number to forward the call to.

    :param str action: The ``action`` attribute takes a URL as an argument.
        When the dialed call ends, Twilio will make a GET or POST request to
        this URL including the parameters below.

        If you provide an ``action`` URL, Twilio will continue the current call
        after the dialed party has hung up, using the TwiML received in your
        response to the ``action`` URL request. Any TwiML verbs occuring after
        a ``<Dial>`` which specifies an ``action`` attribute are unreachable.

        If no ``action`` is provided, ``<Dial>`` will finish and Twilio will
        move on to the next TwiML verb in the document. If there is no next
        verb, Twilio will end the phone call. Note that this is different from
        the behavior of ``<Record>`` and ``<Gather>``. ``<Dial>`` does not make
        a request to the current document's URL by default if no ``action`` URL
        is provided. Instead the call flow falls through to the next TwiML
        verb.

        Request Parameters
        ==================

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the ``action`` URL:

        +------------------+---------------------------------------------------+
        | Parameter        | Description                                       |
        +==================+===================================================+
        | DialCallStatus   | The outcome of the ``<Dial>`` attempt. See the    |
        |                  | ``DialCallStatus`` section below for details.     |
        +------------------+---------------------------------------------------+
        | DialCallSid      | The call sid of the new call leg. This parameter  |
        |                  | is not sent after dialing a conference.           |
        +------------------+---------------------------------------------------+
        | DialCallDuration | The duration in seconds of the dialed call. This  |
        |                  | parameter is not sent after dialing a conference. |
        +------------------+---------------------------------------------------+

        DialCallStatus Values
        =====================

        +-----------+---------------------------------------------------------+
        | Value     | Description                                             |
        +===========+=========================================================+
        | completed | The called party answered the call and was connected to |
        |           | the caller.                                             |
        +-----------+---------------------------------------------------------+
        | busy      | Twilio received a busy signal when trying to connect to |
        |           | the called party.                                       |
        +-----------+---------------------------------------------------------+
        | no-answer | The called party did not pick up before the timeout     |
        |           | period passed.                                          |
        +-----------+---------------------------------------------------------+
        | failed    | Twilio was unable to route to the given phone number.   |
        |           | This is frequently caused by dialing a properly         |
        |           | formated but non-existent phone number.                 |
        +-----------+---------------------------------------------------------+
        | canceled  | The call was canceled via the REST API before it was    |
        |           | answered.                                               |
        +-----------+---------------------------------------------------------+

    :param str method: The ``method`` attribute takes the value 'GET' or
        'POST'. This tells Twilio whether to request the ``action`` URL via
        HTTP GET or POST. This attribute is modeled after the HTML form
        ``method`` attribute. 'POST' is the default value.

    :param int timeout: The ``timeout`` attribute sets the limit in seconds
        that ``<Dial>`` waits for the called party to answer the call.
        Basically, how long should Twilio let the call ring before giving up
        and reporting 'no-answer' as the 'DialCallStatus'.

    :param bool hangup_on_star: The ``hangup_on_star`` attribute lets the
        calling party hang up on the called party by pressing the '*' key on
        his phone. When two parties are connected using ``<Dial>``, Twilio
        blocks execution of further verbs until the caller or called party
        hangs up. This feature allows the calling party to hang up on the
        called party without having to hang up her phone and ending her TwiML
        processing session. When the caller presses '*' Twilio will hang up on
        the called party. If an ``action`` URL was provided, Twilio submits
        'completed' as the 'DialCallStatus' to the URL and processes the
        response. If no ``action`` was provided Twilio will continue on to the
        next verb in the current TwiML document.

    :param int time_limit: The ``time_limit`` attribute sets the maximum
        duration of the ``<Dial>`` in seconds. For example, by setting a time
        limit of 120 seconds ``<Dial>`` will hang up on the called party
        automatically two minutes into the phone call. By default, there is a
        four hour time limit set on calls.

    :param str caller_id: The ``caller_id`` attribute lets you specify the
        caller ID that will appear to the called party when Twilio calls. By
        default, when you put a ``<Dial>`` in your TwiML response to Twilio's
        inbound call request, the caller ID that the dialed party sees is the
        inbound caller's caller ID.

        For example, an inbound caller to your Twilio number has the caller ID
        1-415-123-4567. You tell Twilio to execute a ``<Dial>`` verb to
        1-858-987-6543 to handle the inbound call. The called party
        (1-858-987-6543) will see 1-415-123-4567 as the caller ID on the
        incoming call.

        You are allowed to change the phone number that the called party sees
        to one of the following:

        * Either the 'To' or 'From' number provided in Twilio's TwiML request
          to your app.
        * Any incoming phone number you have purchased from Twilio.
        * Any phone number you have validated with Twilio for use as an
          outgoing caller ID.

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
    """The ``<Dial>`` verb's ``<Conference>`` noun allows you to connect to a
    conference room. Much like how the ``<Number>`` noun allows you to connect
    to another phone number, the ``<Conference>`` noun allows you to connect to
    a named conference room and talk with the other callers who have also
    connected to that room.

    The name of the room is up to you and is namespaced to your account. This
    means that any caller who joins 'room1234' via your account will end up in
    the same conference room, but callers connecting through different accounts
    would not. The maximum number of participants in a single Twilio conference
    room is 40.

    By default, Twilio conference rooms enable a number of useful features used
    by business conference bridges:

        - Conferences do not start until at least two participants join.
        - While waiting, customizable background music is played.
        - When participants join and leave, notification sounds are played to
        - inform the other participants.
        - You can configure or disable each of these features based on your
          particular needs.

    :param str name: Account-wide unique conference name. Callers who enter
        conference rooms with the same name will be placed into the same
        conference room.

    :param bool muted: The ``muted`` attribute lets you specify whether a
        participant can speak on the conference. If this attribute is set to
        ``True``, the participant will only be able to listen to people on the
        conference. This attribute defaults to ``False``.

    :param bool beep: The ``beep`` attribute lets you specify whether a
        notification beep is played to the conference when a participant joins
        or leaves the conference. This defaults to ``True``.

    :param bool start_conference_on_enter: This attribute tells a conference to
        start when this participant joins the conference, if it is not already
        started. This is ``True`` by default. If this is ``False`` and the
        participant joins a conference that has not started, they are muted and
        hear background music until a participant joins where
        ``start_conference_on_enter`` is ``True``. This is useful for
        implementing moderated conferences.

    :param bool end_conference_on_exit: If a participant has this attribute set
        to ``True``, then when that participant leaves, the conference ends and
        all other participants drop out. This defaults to ``False``. This is
        useful for implementing moderated conferences that bridge two calls and
        allow either call leg to continue executing TwiML if the other hangs
        up.

    :param str wait_url: The ``wait_url`` attribute lets you specify a URL for
        music that plays before the conference has started. The URL may be an
        MP3, a WAV or a TwiML document that uses ``<Play>`` or ``<Say>`` for
        content. This defaults to a selection of Creative Commons licensed
        background music, but you can replace it with your own music and
        messages. If the ``wait_url`` responds with TwiML, Twilio will only
        process ``<Play>``, ``<Say>``, and ``<Redirect>`` verbs. ``<Record>``,
        ``<Dial>``, and ``<Gather>`` verbs are not allowed. If you do not wish
        anything to play while waiting for the conference to start, specify the
        empty string (set ``wait_url`` to ``''``).


        If no ``wait_url`` is specified, Twilio will use it's own `HoldMusic
        Twimlet <http://labs.twilio.com/twimlets/holdmusic>`_ that reads a
        public `AWS S3 Bucket <http://s3.amazonaws.com/>`_ for audio files. The
        default ``wait_url`` is:

        http://twimlets.com/holdmusic?Bucket=com.twilio.music.classical

        This URL points at S3 bucket `com.twilio.music.classical
        <http://com.twilio.music.classical.s3.amazonaws.com/>`_, containing a
        selection of nice Creative Commons classical music. Here's a list of S3
        buckets we've assembed with other genres of music for you to choose
        from:

        +-----------------------------------------------------------------------------------------+-------------------------------------------------------------------+
        | Bucket                                                                                  | Twimlet URL                                                       |
        +=========================================================================================+===================================================================+
        | `com.twilio.music.classical <http://com.twilio.music.classical.s3.amazonaws.com/>`_     | http://twimlets.com/holdmusic?Bucket=com.twilio.music.classical   |
        +-----------------------------------------------------------------------------------------+-------------------------------------------------------------------+
        | `com.twilio.music.ambient <http://com.twilio.music.ambient.s3.amazonaws.com/>`_         | http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient     |
        +-----------------------------------------------------------------------------------------+-------------------------------------------------------------------+
        | `com.twilio.music.electronica <http://com.twilio.music.electronica.s3.amazonaws.com/>`_ | http://twimlets.com/holdmusic?Bucket=com.twilio.music.electronica |
        +-----------------------------------------------------------------------------------------+-------------------------------------------------------------------+
        | `com.twilio.music.guitars <http://com.twilio.music.guitars.s3.amazonaws.com/>`_         | http://twimlets.com/holdmusic?Bucket=com.twilio.music.guitars     |
        +-----------------------------------------------------------------------------------------+-------------------------------------------------------------------+
        | `com.twilio.music.rock <http://com.twilio.music.rock.s3.amazonaws.com/>`_               | http://twimlets.com/holdmusic?Bucket=com.twilio.music.rock        |
        +-----------------------------------------------------------------------------------------+-------------------------------------------------------------------+
        | `com.twilio.music.soft-rock <http://com.twilio.music.soft-rock.s3.amazonaws.com/>`_     | http://twimlets.com/holdmusic?Bucket=com.twilio.music.soft-rock   |
        +-----------------------------------------------------------------------------------------+-------------------------------------------------------------------+

    :param str wait_method: This attribute indicates which HTTP method to use
        when requesting ``wait_url``. It defaults to ``POST``. Be sure to use
        ``GET`` if you are directly requesting static audio files such as WAV
        or MP3 files so that Twilio properly caches the files.

    :param int max_participants: This attribute indicates the maximum number of
        participants you want to allow within a named conference room. The
        default maximum number of participants is ``40``. The value must be a
        positive integer less than or equal to ``40``.

        .. note::
            This attribute is currently non-functional, due to a bug in the
            official `twilio-python library
            <https://github.com/twilio/twilio-python>`_. I've submitted a pull
            request to twilio, and once they make a patch for the issue and
            make a PyPI release, I'll update this documentation, and this
            attribute should be functional. For now, if this attribute is
            specified, it will be ignored.

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
