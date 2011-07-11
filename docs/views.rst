=====
Views
=====

In order to help speed up development of your telephony application,
django-twilio ships with a few useful views that you can plug straight into
your project's urlconf, and immediately use!

Teleconferencing
****************

A common development problem for telephony developers has traditionally been
conference rooms--until now. django-twilio provides the simplest possible
teleconferencing solution, and it only requires a single line of code to
implement!

Let's take a look at a few conference patterns, and see how we can easily
implement them into our webapp.

Simple Conference Room
======================

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
======================================

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
====================================

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
    from twilio import Response
    from django_twilio.decorators import twilio_view

    @twilio_view
    def say_hi(request):
        r = Response()
        r.addSay('Thanks for joining the conference! Django and twilio rock!')
        return r

If you run this example code, you'll notice that when you call your
application, twilio first says "Thanks for joining the conference..." before
joining you--pretty neat, eh?

As you can see, this is a great way to build custom logic into your conference
room call flow. One pattern that is commonly requested is to play an estimated
wait time--a simple project using :func:`django_twilio.views.conference`.

Other Conferencing Goodies
==========================

Now may be a good time to check out the API docs for
:func:`django_twilio.views.conference` to see all the other goodies available.

Grabbing Caller Input
*********************

As you begin to build more and more complicated telephony applications, you'll
need a way to accept caller input via their telephone touch pad. For this
purpose, django-twilio ships with the :func:`django_twilio.views.gather` view.

Below we'll look at a few examples displaying proper usage.

Collecting Touchtone Input
==========================

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
===============================

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

Playing Audio
*************

django-twilio makes it easy to play audio files to callers. Below, we'll look
at two examples which demonstrate how to do so using the excellent
:func:`django_twilio.views.play` view.

Playing a WAV File
==================

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
=============

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

Saying Stuff
************

In a majority of telephony apps--you'll want to say something. It can be tedious
to record your own voice prompts for every bit of call flow, which is why you'll
want to use django-twilio's :func:`django_twilio.views.say` view.

The :func:`django_twilio.views.say` view allows you to simply "say stuff" in a
variety of languages (in either a male or female voice).

Hello, World!
=============

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
=================================

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
==============

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
