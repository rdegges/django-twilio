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
        url(r'^/conference/(?P<name>\w+)/$', 'django_twilio.views.conference'),
        # ...
    )

2. Now, log into your `twilio dashboard
   <https://www.twilio.com/user/account/apps>`_ and create a new app. Point the
   voice URL of your app at http://yourserver.com/conference/business/.

3. Call your new application's phone number. twilio will send a HTTP POST
   request to your web server at ``/conference/business/``, and you should be
   dumped into your new conference room!

Pretty easy eh? No coding even required!
