How To...
=========

This section documents lots of common "How do I..." questions. Since
``django-twilio`` has a lot of native functionality, some features that don't
necessarily fit into other parts of the documentation are only documented here.

Blacklist Callers
-----------------

One common problem is dealing with users who abuse services. Regardless of what
your telephony app does, it can be dangerous and expensive to run your
application without the ability to blacklist users.

Luckily, ``django-twilio`` provides built-in blacklist functionality, and will
fit your needs (whatever they may be).

Hypothetical Abuse Scenario
---------------------------

Let's say you run a Twilio app that forwards calls from your Twilio toll-free
number to your private business number. Since you have to pay for Twilio calls,
it could potentially become very expensive for you if a caller repeatedly calls
your toll-free number, causing you to quickly drain your account balance.

Blacklisting Callers via Django Admin
-------------------------------------

The simplest way to blacklist callers is via the Django admin panel. If you're
using the Django admin panel, you'll see a ``django-twilio`` Caller section that
allows you to manage callers.

To blacklist a caller, do the following:

1. Click the ``Add`` button next to the ``Caller`` object in the admin panel.
   If you're running the server locally, the URL would be:
   http://localhost:8000/admin/django_twilio/caller/add/.
2. Enter in the caller's details that you wish to block. The phone number should
   be of the form: ``+1NXXNXXXXXX`` (`E.164 format
   <http://en.wikipedia.org/wiki/E.164>`_).
3. Check the ``blacklisted`` box.
4. Click the ``Save`` button.

Now any ``django-twilio`` built-in views or decorators will automatically
reject calls from the specified caller!

.. note::
   This does NOT effect code that does NOT use ``django-twilio``. For example,
   if you write code that places outbound calls or SMS messages, since your code
   won't be interacting with ``django-twilio``, the blacklist will NOT be
   honored.
