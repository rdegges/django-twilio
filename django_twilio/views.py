from twilio import Conference, Dial, Response
from django_twilio.decorators import twilio_view


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
    d = Dial()
    d.append(Conference(
        name = name,
        muted = muted,
        beep = beep,
        startConferenceOnEnter = start_conference_on_enter,
        endConferenceOnExit = end_conference_on_exit,
        waitUrl = wait_url,
        waitMethod = wait_method,
    ))
    r.append(d)
    return r


@twilio_view
def gather(request, action=None, method=None, num_digits=None, timeout=None,
        finish_on_key=None):
    """The ``<Gather>`` verb collects digits that a caller enters into his or
    her telephone keypad. When the caller is done entering data, Twilio submits
    that data to the provided ``action`` URL in an HTTP GET or POST request,
    just like a web browser submits data from an HTML form.

    If no input is received before timeout, ``<Gather>`` falls through to the
    next verb in the TwiML document.

    You may optionally nest ``<Say>`` and ``<Play>`` verbs within a
    ``<Gather>`` verb while waiting for input. This allows you to read menu
    options to the caller while letting her enter a menu selection at any time.
    After the first digit is received the audio will stop playing.

    :param str action: The ``action`` attribute takes an absolute or relative
        URL as a value. When the caller has finished entering digits Twilio
        will make a GET or POST request to this URL including the parameters
        below. If no ``action`` is provided, Twilio will by default make a POST
        request to the current document's URL.

        After making this request, Twilio will continue the current call using
        the TwiML received in your response. Keep in mind that by default
        Twilio will re-request the current document's URL, which can lead to
        unwanted looping behavior if you're not careful. Any TwiML verbs
        occuring after a ``<Gather>`` are unreachable, unless the caller enters
        no digits.

        If the ``timeout`` is reached before the caller enters any digits, or
        if the caller enters the ``finish_on_key`` value before entering any
        other digits, Twilio will not make a request to the ``action`` URL but
        instead continue processing the current TwiML document with the verb
        immediately following the ``<Gather>``.

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the ``action`` URL:

        +-----------+---------------------------------------------------------------------------+
        | Parameter | Description                                                               |
        +===========+===========================================================================+
        | Digits    | The digits the caller pressed, excluding the finish_on_key digit if used. |
        +-----------+---------------------------------------------------------------------------+

    :param str method: The ``method`` attribute takes the value 'GET' or
        'POST'. This tells Twilio whether to request the ``action`` URL via
        HTTP GET or POST. This attribute is modeled after the HTML form
        ``method`` attribute. 'POST' is the default value.

    :param int timeout: The ``timeout`` attribute sets the limit in seconds
        that Twilio will wait for the caller to press another digit before
        moving on and making a request to the ``action`` URL. For example, if
        ``timeout`` is 10, Twilio will wait ten seconds for the caller to press
        another key before submitting the previously entered digits to the
        ``action`` URL. Twilio waits until completing the execution of all
        nested verbs before beginning the timeout period.

    :param str finish_on_key: The ``finish_on_key`` attribute lets you choose
        one value that submits the received data when entered. For example, if
        you set ``finish_on_key`` to '#' and the user enters '1234#', Twilio
        will immediately stop waiting for more input when the '#' is received
        and will submit "Digits=1234" to the ``action`` URL. Note that the
        ``finish_on_key`` value is not sent. The allowed values are the digits
        0-9, '#' , '*' and the empty string (set ``finish_on_key`` to ''). If
        the empty string is used, ``<Gather>`` captures all input and no key
        will end the ``<Gather>`` when pressed. In this case Twilio will submit
        the entered digits to the ``action`` URL only after the timeout has
        been reached. The default ``finish_on_key`` value is '#'. The value can
        only be a single character.

    :param int num_digits: The ``num_digits`` attribute lets you set the number
        of digits you are expecting, and submits the data to the ``action`` URL
        once the caller enters that number of digits. For example, one might
        set ``num_digits`` to 5 and ask the caller to enter a 5 digit zip code.
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
    r.addGather(action=action, method=method, numDigits=num_digits,
            timeout=timeout, finishOnKey=finish_on_key)
    return r


@twilio_view
def play(request, url, loop=None):
    """The <Play> verb plays an audio file back to the caller. Twilio retrieves
    the file from a URL that you provide.

    :param str url: The URL of an audio file that Twilio will retrieve and play
        to the caller.

    :param int loop: The ``loop`` attribute specifies how many times the audio
        file is played. The default behavior is to play the audio once.
        Specifying 0 will cause the the ``<Play>`` verb to loop until the call
        is hung up.

    Twilio supports the following audio MIME types for audio files retrieved by
    the ``<Play>`` verb:

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
    r.addPlay(url, loop=loop)
    return r


@twilio_view
def record(request, action=None, method=None, timeout=None, finish_on_key=None,
        max_length=None, transcribe=None, transcribe_callback=None,
        play_beep=None):
    """The ``<Record>`` verb records the caller's voice and returns to you the
    URL of a file containing the audio recording. You can optionally generate
    text transcriptions of recorded calls by setting the ``transcribe``
    attribute of the ``<Record>`` verb to 'true'.

    :param str action: The ``action`` attribute takes an absolute or relative
        URL as a value. When recording is finished Twilio will make a GET or
        POST request to this URL including the parameters below. If no
        ``action`` is provided, ``<Record>`` will default to requesting the
        current document's URL.

        After making this request, Twilio will continue the current call using
        the TwiML received in your response. Keep in mind that by default
        Twilio will re-request the current document's URL, which can lead to
        unwanted looping behavior if you're not careful. Any TwiML verbs
        occuring after a ``<Record>`` are unreachable.

        There is one exception: if Twilio receives an empty recording, it will
        not make a request to the ``action`` URL. The current call flow will
        continue with the next verb in the current TwiML document.

        Request Parameters
        ==================

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the ``action`` URL:

        +-------------------+---------------------------------------------------------------------------------+
        | Parameter         | Description                                                                     |
        +===================+=================================================================================+
        | RecordingUrl      | the URL of the recorded audio                                                   |
        +-------------------+---------------------------------------------------------------------------------+
        | RecordingDuration | the time duration of the recorded audio                                         |
        +-------------------+---------------------------------------------------------------------------------+
        | Digits            | the key (if any) pressed to end the recording or 'hangup' if the caller hung up |
        +-------------------+---------------------------------------------------------------------------------+

    :param str method: The ``method`` attribute takes the value 'GET' or
        'POST'. This tells Twilio whether to request the ``action`` URL via
        HTTP GET or POST. This attribute is modeled after the HTML form
        ``method`` attribute. 'POST' is the default value.

    :param int timeout: The ``timeout`` attribute tells Twilio to end the
        recording after a number of seconds of silence has passed. The default
        is 5 seconds.

    :param str finish_on_key: The ``finish_on_key`` attribute lets you choose a
        set of digits that end the recording when entered. For example, if you
        set ``finish_on_key`` to '#' and the caller presses '#', Twilio will
        immediately stop recording and submit 'RecordingUrl',
        'RecordingDuration', and the '#' as parameters in a request to the
        ``action`` URL. The allowed values are the digits 0-9, '#' and '*'. The
        default is '1234567890*#' (i.e. any key will end the recording). Unlike
        ``<Gather>``, you may specify more than one character as a
        ``finish_on_key`` value.

    :param int max_length: The ``max_length`` attribute lets you set the
        maximum length for the recording in seconds. If you set ``max_length``
        to 30, the recording will automatically end after 30 seconds of
        recorded time has elapsed. This defaults to 3600 seconds (one hour) for
        a normal recording and 120 seconds (two minutes) for a transcribed
        recording.

    :param bool transcribe: The ``transcribe`` attribute tells Twilio that you
        would like a text representation of the audio of the recording. Twilio
        will pass this recording to our speech-to-text engine and attempt to
        convert the audio to human readable text. The ``transcribe`` option is
        off by default. If you do not wish to perform transcription, simply do
        not include the transcribe attribute.

        .. note::
            Transcription is a pay feature. If you include a ``transcribe`` or
            ``transcribe_callback`` attribute on your verb your account will be
            charged. See the `pricing page
            <http://www.twilio.com/pricing-signup>`_ for our transcription
            prices.

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
        Transcriptions section), but Twilio will not asynchronously notify your
        application.

        Request Parameters
        ==================

        Twilio will pass the following parameters in addition to the standard
        TwiML Voice request parameters with its request to the
        ``transcribe_callback`` URL:

        +---------------------+--------------------------------------------------------------------------+
        | Parameter           | Description                                                              |
        +=====================+==========================================================================+
        | TranscriptionText   | Contains the text of the transcription.                                  |
        +---------------------+--------------------------------------------------------------------------+
        | TranscriptionStatus | The status of the transcription attempt: either 'completed' or 'failed'. |
        +---------------------+--------------------------------------------------------------------------+
        | TranscriptionUrl    | The URL for the transcription's REST API resource.                       |
        +---------------------+--------------------------------------------------------------------------+
        | RecordingUrl        | The URL for the transcription's source recording resource.               |
        +---------------------+--------------------------------------------------------------------------+

    :param bool play_beep: The ``play_beep`` attribute allows you to toggle
        between playing a sound before the start of a recording. If you set the
        value to ``False``, no beep sound will be played.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^record/$', 'django_twilio.views.record'),
            # ...
        )
    """
    pass


@twilio_view
def say(request, text, voice=None, language=None, loop=None):
    """The ``<Say>`` verb converts text to speech that is read back to the
    caller. ``<Say>`` is useful for development or saying dynamic text that is
    difficult to pre-record.

    :param str text: The text Twilio will read to the caller. Limited to 4KB.

    :param str voice: The ``voice`` attribute allows you to choose a male or
        female voice to read text back. The default value is 'man'.

    :param str language: The ``language`` attribute allows you pick a voice
        with a specific language's accent and pronunciations. Twilio currently
        supports languages 'en' (English), 'es' (Spanish), 'fr' (French), and
        'de' (German). The default is 'en'.

    :param int loop: The ``loop`` attribute specifies how many times you'd like
        the text repeated. The default is once. Specifying 0 will cause the the
        ``<Say>`` verb to loop until the call is hung up.

    Usage::

        # urls.py
        urlpatterns = patterns('',
            # ...
            url(r'^say/$', 'django_twilio.views.say', {'text': 'hello, world!'})
            # ...
        )
    """
    r = Response()
    r.addSay(text, voice=voice, language=language, loop=loop)
    return r
