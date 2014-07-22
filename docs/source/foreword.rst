========
Foreword
========

Read this before you get started with ``django-twilio``. This will hopefully
answer some questions about the purpose of the project, and why you should (or
shouldn't) be using it.

Purpose
=======

Building telephony applications has always been something of a complex and time
consuming task for developers. With the advent of `Twilio
<http://www.twilio.com/>`_, developers were able to build large scale telephony
applications for the first time, without the massive learning curve associated
with traditional telephony development.

While Twilio's APIs allow you to build powerful voice and SMS apps in your
favorite programming language, it can still be quite difficult and time
consuming to roll out your own telephony apps for your
`Django <https://www.djangoproject.com/>`_-powered website.

The core purpose of ``django-twilio`` is to abstract away as much telephony
knowledge as possible, so that you can focus on the functionality and logic of
your telephony app, and have it seamlessly integrate into your website without
confusion.

Use Case
========

``django-twilio`` is a complete solution for anyone who wants to integrate
voice or SMS functionality into their Django website without requiring any
additional infrastructure.

Here are some common use cases:

* You want to build one or more telephone conference rooms for talking with
  co-workers or clients.
* You want be able to accept SMS messages from your clients, and respond to
  them programmatically.
* You want to record important phone calls (incoming or outgoing) and store
  the recordings for analysis.
* You want to track telephone marketing campaigns, and review detailed data.
* You want to build rich, interactive telephone systems. (EG: "Press 1 to talk
  with a sales agent, press 2 to schedule a reservation, press 3 to purchase a
  hat.")
* And many more.

Prerequisite Knowledge
======================

Before getting started with ``django-twilio``, it will serve you best to read
the `How it Works <http://www.twilio.com/api/>`_ page on Twilio's website. That
describes the architecture and API flow that all of your applications will be
using, and that ``django-twilio`` will help to abstract.

``django-twilio`` also depends on the official `Twilio python library
<http://readthedocs.org/docs/twilio-python/en/latest/>`_, so you may want to
familiarize yourself with their docs before continuing so you have a good idea
of how things work.

Other than that, you're good to go!
