Accessing Twilio Resources
==========================

Let's say you're building a Twilio application that needs access to all of your
account data -- stuff like call logs, recordings, SMS messages, etc.
``django-twilio`` makes accessing this information extremely easy.


The Twilio REST Client
----------------------

The official `Twilio python library
<http://readthedocs.org/docs/twilio-python/en/latest/>`_ provides a really
awesome wrapper around Twilio's REST API. Before continuing on, you may want to
read the `official documentation
<http://readthedocs.org/docs/twilio-python/en/latest/usage/basics.html>`_ for
this feature, as understanding this will make the documentation below
significantly easier to follow.


How it Works
------------

If you are using the `Twilio python library
<http://readthedocs.org/docs/twilio-python/en/latest/>`_ by itself (without
``django-twilio``), you could see a list of all the phone numbers you have
provisioned to your Twilio account by running the following code::

    from twilio.rest import TwilioRestClient


    # Your private Twilio API credentials.
    ACCOUNT_SID = 'xxx'
    AUTH_TOKEN = 'xxx'

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    for number in client.phone_numbers.iter():
        print(number.friendly_name)

While this is really convenient, it breaks the `Don't Repeat Yourself
<http://en.wikipedia.org/wiki/Don't_repeat_yourself>`_ rule of software
engineering by making you manually specify your account credentials.

Since ``django-twilio`` already requires you to enter your Twilio credentials in
your ``settings.py`` file, ``django-twilio`` provides a simple wrapper around
``TwilioRestClient``: ``django_twilio.client.twilio_client``.


The ``twilio_client`` Wrapper
-----------------------------

As mentioned in the previous section, ``django-twilio`` ships with an
instantiated ``TwilioRestClient``, so that you can use the `Twilio REST API
<http://readthedocs.org/docs/twilio-python/en/latest/usage/basics.html>`_ with
as little effort as possible. :)

Using ``django_twilio.client.twilio_client``, you can print a list of all
the phone numbers you have provisioned to your Twilio account by running the
following code::

    from django_twilio.client import twilio_client


    for number in twilio_client.phone_numbers.iter():
        print(number.friendly_name)

See how you didn't have to worry about credentials or anything? Niiiiice.


Further Reading
---------------

Twilio's REST API lets you do a lot of awesome stuff. Among other things, you
can:

* View and manage your Twilio account and sub-accounts.
* Manage your Twilio applications.
* Authorize Twilio apps.
* View your call logs.
* View all of your authorized caller IDs.
* Check out your connected apps.
* View all Twilio notifications.
* Get a list of all call recordings.
* View all call transcriptions.
* View all SMS messages.
* View and manage all phone numbers.
* Manage your conference rooms.
* Manage your API sandboxes.
* etc...

To learn more about what you can do, I suggest reading the `Twilio REST
documentation <https://www.twilio.com/docs/api/rest>`_ and the `twilio-python
REST documentation
<https://twilio-python.readthedocs.org/en/latest/usage/basics.html>`_.
