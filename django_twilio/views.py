from twilio import Conference, Dial, Response
from django_twilio.decorators import twilio_view


@twilio_view
def conference(request, name, muted=None, beep=None,
        start_conference_on_enter=None, end_conference_on_exit=None,
        wait_url=None, wait_method=None, max_participants=None):
    """A fully featured conference room.

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
            url(r'^conference/?(P<name>\w+)/$', 'django_twilio.views.conference',
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
def say(request, text, voice=None, language=None, loop=None):
    """The ``<Say>`` verb converts text to speech that is read back to the
    caller. ``<Say>`` is useful for development or saying dynamic text that is
    difficult to pre-record.

    :param str voice: The ``voice`` attribute allows you to choose a male or
        female voice to read text back. The default value is 'man'.

    :param str language: The ``language`` attribute allows you pick a voice
        with a specific language's accent and pronunciations. Twilio currently
        supports languages 'en' (English), 'es' (Spanish), 'fr' (French), and
        'de' (German). The default is 'en'.

    :param int loop: The ``loop`` attribute specifies how many times you'd like
        the text repeated. The default is once. Specifying 0 will cause the the
        ``<Say>`` verb to loop until the call is hung up.
    """
    pass
