Views
=====

In order to help speed up development of your telephony application,
django-twilio ships with a few useful views that you can plug straight into
your project's urlconf, and immediately use!

Saying Stuff
------------

In a majority of telephony apps--you'll want to say something. It can be tedious
to record your own voice prompts for every bit of call flow, which is why you'll
want to use django-twilio's :func:`django_twilio.views.say` view.

The :func:`django_twilio.views.say` view allows you to simply "say stuff" in a
variety of languages (in either a male or female voice).

Hello, World!
*************

Let's take a look at a *classic* example::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^hello_world/$', 'django_twilio.views.say', {
            'text': 'Hello, world!'
        }),
        # ...
    )

Hook a twilio number up to that URL, and you'll hear a man say "Hello, world!"
when called. Nice!

Changing the Voice (and Language)
*********************************

By default, twilio reads off all text in the English language in a man's voice.
By it's easy to change that. In the example below, we'll say "goodbye" in
Spanish, with a female voice::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^goodbye/$', 'django_twilio.views.say', {
            'text': 'Adios!',
            'voice': 'woman',
            'language': 'es',
        }),
        # ...
    )

Simple, right?

Repeating Text
**************

On occasion, you'll also want to repeat some text, without copy+paste. In this
situation, you can simply specify an optional ``loop`` parameter::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^lol/$', 'django_twilio.views.say', {
            'text': 'lol',
            'loop': 0,  # 0 = Repeat forever, until hangup :)
        }),
        # ...
    )

In this example, we'll just keep repeating "lol" to the caller until they hang
up.

For more information, be sure to read the API docs on
:func:`django_twilio.views.say`.

Playing Audio
-------------

django-twilio makes it easy to play audio files to callers. Below, we'll look
at two examples which demonstrate how to do so using the excellent
:func:`django_twilio.views.play` view.

Playing a WAV File
******************

In this example, we'll play a simple WAV file to a caller. For simplicity's
sake, just assume that this WAV file actually exists::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^play/$', 'django_twilio.views.play', {
            'url': 'http://mysite.com/greeting.wav',
        })
        # ...
    )

Assuming the url http://mysite.com/greeting.wav exists, and is a legitimate
WAV file, when you call your twilio application, you should hear the audio
file play.

.. note::
    You can play lots of different types of audio files. For a full list of the
    formats twilio accepts, look at the API reference material for the
    :func:`django_twilio.views.play` view.

Looping Audio
*************

In this example, we'll play the same greeting audio clip as we did above, but
this time--we'll loop it 3 times::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^play/$', 'django_twilio.views.play', {
            'url': 'http://mysite.com/greeting.wav',
            'loop': 3,
        })
        # ...
    )

Not too bad (for no code)!

Grabbing Caller Input
---------------------

As you begin to build more and more complicated telephony applications, you'll
need a way to accept caller input via their telephone touch pad. For this
purpose, django-twilio ships with the :func:`django_twilio.views.gather` view.

Below we'll look at a few examples displaying proper usage.

Collecting Touchtone Input
**************************

The simplest thing we can do using the :func:`django_twilio.views.gather` view
is to collect caller touchtone input until the caller stops hitting keys. To do
this, we can write our URLconf as follows::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^gather/$', 'django_twilio.views.gather'),
        # ...
    )

By default--once the caller finishes entering their input, twilio will send a
HTTP POST request to the same URL. So in our example above, if a caller enters
'666#', then twilio would send a POST request to our ``/gather/`` URL with a
``Digits`` parameter that contains the value '666#'.

Redirect After Collecting Input
*******************************

Let's say that instead of POST'ing the caller's input to the same URL, you want
to instead POST the data to another URL (or view). No problem! In fact, we'll
even tell twilio to send the data in GET format instead of POST::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^gather/$', 'django_twilio.views.gather', {
            'action': '/process_input/',
            'method': 'GET',
        }),
        url(r'^process_input/$', 'mysite.myapp.views.process'),
        # ...
    )

    # mysite.myapp.views.py
    from django.http import HttpResponse

    def process(request):
        print request.GET   # Output GET data to terminal (for debug).
        return HttpResponse()

If you test out this application, you'll see that the caller's input is sent
(via HTTP GET) to the ``process`` view once the input has been collected.

Controlling Input Patterns
**************************

Lastly, the :func:`django_twilio.views.gather` view allows you to control
various aspects of the input collection process.

Our example below:

* Limits the amount of seconds that twilio will wait for the caller to press
  another digit to 5. If no input is entered after 5 seconds, then twilio will
  automatically pass the data along to the URL specified in the ``action``
  parameter.
* Automatically end the input collection process if the caller hits the '#' key.
  This way, if the caller enters '12345#', regardless of what the ``timeout``
  parameter is set to, twilio will pass the data along to the URL specified in
  the ``action`` parameter.
* Limit the total amount of digits collected to 10. Once 10 digits has been
  reached, twilio will pass the data along to the URL specified in the
  ``action`` parameter.

::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^gather/$', 'django_twilio.views.gather', {
            'action': '/process_input/',
            'method': 'GET',
            'timeout': 5,
            'finish_on_key': '#',
            'num_digits': 10,
        }),
        # ...
    )

Recording Calls
---------------

django-twilio also comes with a built-in call recording view:
:func:`django_twilio.views.record`. In the examples below, we'll walk through
plugging the :func:`django_twilio.views.record` view into our fictional Django
website in a variety of situations.

Record a Call
*************

Let's start simple. In this example, we'll setup our URLconf to record our call,
then hit another URL in our application to provide TwiML instructions for
twilio::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^record/$', 'django_twilio.views.record', {
            'action': '/call_john/',
            'play_beep': True,
        })
        # ...
    )

If we call our application, twilio will start recording our call (after playing
a beep), then send a POST request to our ``/call_john/`` URL and continue
executing call logic. This allows us to start recording, then continue on
passing instructions to twilio (maybe we'll call our lawyer :)).

Stop Recording on Silence
*************************

In most cases, you'll only want to record calls that actually have talking in
them. It's pointless to record silence. That's why twilio provides a ``timeout``
parameter that we can use with django-twilio's
:func:`django_twilio.views.record` view::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^record/$', 'django_twilio.views.record', {
            'action': '/call_john/',
            'play_beep': True,
            'timeout': 5,   # Stop recording after 5 seconds of silence
                            # (default).
        })
        # ...
    )

By default, twilio will stop the recording after 5 seconds of silence have been
detected--but you can easily adjust this number as you see fit. If you're
planning on recording calls that may include hold times or other things, then
you should probably bump this number up to avoid ending the recording if you get
put on hold.

Transcribe Your Call Recording
******************************

On occasion, you may want to transcribe your call recordings. Maybe you're
making a call to your secretary to describe your TODO list, and want to ensure
you get it in text format--or maybe you're just talking with colleagues about
how to best destroy the earth. Whatever the situation may be, twilio's got you
covered!

In this example, we'll record our call, and force twilio to transcribe it after
we hang up. We'll also give twilio a URL to POST to once it's finished
transcribing, so that we can do some stuff with our transcribed text (maybe
we'll email it to ourselves, or something).

.. note::
    Transcribing is a **paid** feature. See twilio's `pricing page
    <http://www.twilio.com/pricing-signup>`_ for the current rates. Also--twilio
    limits transcription time to 2 minutes or less. If you set the
    ``max_length`` attribute to > 120 (seconds), then twilio will **not**
    transcribe your call, and will instead write an error to your debug log (in
    the twilio web panel).

::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^record/$', 'django_twilio.views.record', {
            'action': '/call_john/',
            'play_beep': True,
            'transcribe': True,
            'transcribe_callback': '/email_call_transcription/',
        })
        # ...
    )

Sending SMS Messages
--------------------

In addition to building plug-n-play voice applications, we can also build
plug-n-play SMS applications using the :func:`django_twilio.views.sms` view.
This view allows us to send off arbitrary SMS messages based on incoming twilio
requests.

Reply With a SMS
****************

This example demonstrates a simple SMS reply. Whenever twilio sends us an
incoming request, we'll simply send back a SMS message to the sender::

    urlpatterns = patterns('',
        # ...
        url(r'^sms/$', 'django_twilio.views.sms', {
            'message': 'Thanks for the SMS. Talk to you soon!',
        }),
        # ...
    )

Sending SMS Messages (with Additional Options)
**********************************************

Like most of our other views, the :func:`django_twilio.views.sms` view also
allows us to specify some other parameters to change our view's behavior::

    urlpatterns = patterns('',
        # ...
        url(r'^sms/$', 'django_twilio.views.sms', {
            'message': 'Yo!',
            'to': '+12223334444',
            'sender': '+18882223333',
            'status_callback': '/sms/completed/',
        }),
        # ...
    )

Here, we instruct django-twilio to send a SMS message to the caller
'+1-222-333-4444' from the sender '+1-888-222-3333'. As you can see,
django-twilio allows you to fully customize the SMS sending.

Furthermore, the ``status_callback`` parameter that we specified will be POST'ed
to by twilio once it attempts to send this SMS message. twilio will send us some
metadata about the SMS message that we can use in our application as desired.

Teleconferencing
----------------

A common development problem for telephony developers has traditionally been
conference rooms--until now. django-twilio provides the simplest possible
teleconferencing solution, and it only requires a single line of code to
implement!

Let's take a look at a few conference patterns, and see how we can easily
implement them into our webapp.

Simple Conference Room
**********************

Let's say you want to build the world's simplest conference room. It would
consist of nothing more than a phone number that, when called, dumps the
callers into a conference room and let's them chat with each other.

Assuming you've already installed django-twilio, here's how you can build this
simple conference room:

1. Edit your project's ``urls.py`` and add the following::

    urlpatterns = patterns('',
        # ...
        url(r'^conference/(?P<name>\w+)/$', 'django_twilio.views.conference'),
        # ...
    )

2. Now, log into your `twilio dashboard
   <https://www.twilio.com/user/account/apps>`_ and create a new app. Point the
   voice URL of your app at http://yourserver.com/conference/business/.

3. Call your new application's phone number. twilio will send a HTTP POST
   request to your web server at ``/conference/business/``, and you should be
   dumped into your new *business* conference room!

Pretty easy eh? No coding even required!

Simple Conference Room with Rock Music
**************************************

Let's face it, the simple conference you just built was pretty cool, but the
music that twilio plays by default is pretty boring. While you're waiting for
other participants to join the conference, you probably want to listen to some
rock music, right?

Luckily, that's a quick fix!

Open up your ``urls.py`` once more, and add the following::

    urlpatterns = patterns('',
        # ...
        url(r'^conference/(?P<name>\w+)/$', 'django_twilio.views.conference', {
            'wait_url': 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.rock',
            'wait_method': 'GET',
        })
        # ...
    )

:func:`django_twilio.views.conference` allows you to specify optional
parameters easily in your urlconf. Here, we're using the ``wait_url`` parameter
to instruct twilio to play the rock music while the participant is waiting for
other callers to enter the conference. The ``wait_method`` parameter is simply
for efficiency's sake--telling twilio to use the HTTP GET method (instead of
POST, which is the default), allows twilio to properly cache the sound files.

Conference Room with Custom Greeting
************************************

Messing around with hold music is fine and dandy, but it's highly likely that
you'll need to do more than that! In the example below, we'll outline how to
build a conference room that greets each user before putting them into the
conference.

This example shows off how flexible our views can be, and how much we can do
with just the build in :func:`django_twilio.views.conference` view::

    # urls.py
    urlpatterns = patterns('',
        # ...
        url(r'^say_hi/$', 'mysite.views.say_hi'),
        url(r'^conference/(?P<name>\w+)/$', 'django_twilio.views.conference', {
            'wait_url': 'http://yoursite.com/say_hi/',
        })
        # ...
    )

    # views.py
    from twilio.twiml import Response
    from django_twilio.decorators import twilio_view

    @twilio_view
    def say_hi(request):
        r = Response()
        r.say('Thanks for joining the conference! Django and twilio rock!')
        return r

If you run this example code, you'll notice that when you call your
application, twilio first says "Thanks for joining the conference..." before
joining you--pretty neat, eh?

As you can see, this is a great way to build custom logic into your conference
room call flow. One pattern that is commonly requested is to play an estimated
wait time--a simple project using :func:`django_twilio.views.conference`.

Other Conferencing Goodies
**************************

Now may be a good time to check out the API docs for
:func:`django_twilio.views.conference` to see all the other goodies available.
