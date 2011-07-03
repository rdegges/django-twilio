========
Foreword
========

Read this before you get started with django-twilio. This will hopefully answer
some questions about the purpose of the project, and why you should (or
shouldn't) be using it.

Purpose
=======

Building telephony applications has always been something of a complex and time
consuming task for developers. With `twilio <http://www.twilio.com/>`_'s entry
into the telephony world, developers were able to build large scale telephony
applications for the first time, without the massive learning curve associated
with traditional telephony development.

While twilio's APIs allow you to build powerful voice & sms apps in your
favorite programming language, it can still be quite difficult and time
consuming to roll out your own telephony apps for your Django-powered website.

django-twilio's core purpose is to abstract away as much telephony knowledge as
possible, so that you can focus on the functionality and logic of your
telephony app, and have it seamlessly integrate into your website without
confusion.

Use Case
========

django-twilio is a complete solution for anyone who wants to integrate voice or
SMS functionality into their website without requiring any additional
infrastructure.

Here are some common use cases:

* You want to build one or more telephone conference rooms for talking with
  co-workers or clients.
* You want be able to accept SMS messages from your clients, and respond to
  them pragmatically.
* You want to record import phone calls (incoming or outgoing) and store the
  call recordings for analysis.
* You want to track telephone marketing campaigns, and review detailed data.
* You want to build rich, interactive telephone systems. (EG: "Press 1 to talk
  with a sales agent, press 2 to schedule a reservation, press 3 to purchase a
  hat.")
* And many more.
