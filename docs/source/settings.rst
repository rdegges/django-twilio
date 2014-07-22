Settings
========

Django-twilio has various settings that can be used to turn features on and off.

Here we explain each setting, its requirement, and why you might want to use it.

Each setting should be placed in your ``settings.py`` file, except the
``TWILIO_ACCOUNT_SID`` and ``TWILIO_AUTH_TOKEN`` variables, which should be kept
in your environment variables to ensure their security.


TWILIO_ACCOUNT_SID (REQUIRED)
-----------------------------

The ``TWILIO_ACCOUNT_SID`` setting is required, and will throw an exception if
it is not configured correctly::

    TWILIO_ACCOUNT_SID = 'SIDXXXXXXXXXXXXXXX'

This setting is used to authenticate your Twilio account.

   .. note::
      This setting can be placed in your Python environment instead, if you wish.
      This is a far more secure option, and is recommended.

To add this setting to your environment, using ``virtualenv`` open up your
``/bin/activate.sh`` file and add the following to the end::

    export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXX


TWILIO_AUTH_TOKEN (REQUIRED)
----------------------------

The ``TWILIO_AUTH_TOKEN`` setting is required, and will throw an exception if
it is not configured correctly::

    TWILIO_AUTH_TOKEN = 'ATXXXXXXXXXXXXXXX'

This setting is used to authenticate your Twilio account.

   .. note::
      This setting can be placed in your Python environment instead, if you wish.
      This is a far more secure option, and is recommended.

Using ``virtualenv`` open up your ``/bin/activate.sh`` file and add the following
to the end::

    export TWILIO_AUTH_TOKEN=XXXXXXXXXXXXX

DJANGO_TWILIO_FORGERY_PROTECTION (optional)
-------------------------------------------

The ``DJANGO_TWILIO_FORGERY_PROTECTION`` setting is optional. This setting is a
boolean, and should be placed in the ``settings.py`` file:

    DJANGO_TWILIO_FORGERY_PROTECTION = False

This setting is used to determine the forgery protection used by
``django-twilio``. If not set, this will always be the opposite of
``settings.DEBUG``, so in production mode the forgery protection will be on, and
in debug mode the protection will be turned off.

It is recommended that you leave the protection off in debug mode, but this
setting will allow you to test the forgery protection with a tool like `ngrok
<http://ngrok.com>`_

DJANGO_TWILIO_BLACKLIST_CHECK (optional)
----------------------------------------

The ``DJANGO_TWILIO_BLACKLIST_CHECK`` setting is optional. This setting is a
boolean, and should be placed in the ``settings.py`` file::

    DJANGO_TWILIO_BLACKLIST_CHECK = True

This setting will determine if ``django-twilio`` will run a database query
comparing the incoming request ``From`` attribute with any potential
:class:`Caller` objects in your database.

In short: turning this off will remove an unnecessary database query if you are not
using any blacklists.
