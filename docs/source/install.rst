Installation
============

Installing ``django-twilio`` is simple.

Firstly, download and install the ``django-twilio`` package.

The easiest way is with `pip
<http://www.pip-installer.org/en/latest/>`_ ::

    $ python -m pip install django-twilio


Requirements
------------

``django-twilio`` will automatically install the official `twilio-python library
<https://github.com/twilio/twilio-python>`_. The ``twilio-python`` library helps you
rapidly build Twilio applications, and it is heavily suggested that you check
out that project before using ``django-twilio``.


Django Integration
------------------

After ``django-twilio`` is installed, add it to your ``INSTALLED_APPS`` tuple in
your ``settings.py`` file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'django_twilio',
        ...
    )

.. note::
    Please note the underscore!

Databases
------------------------

Django has built in migrations, so there is no need to install any
third-party schema management tool. To sync the ``django-twilio`` models
with your Django project, just run::

    $ python manage.py migrate

Upgrading
---------

Upgrading ``django-twilio`` gracefully is easy using pip::

    $ python -m pip install --upgrade django-twilio

Then you just need to update the models::

    $ python manage.py migrate django_twilio


Authentication Token Management
-------------------------------

``django-twilio`` offers multiple ways to add your Twilio credentials to your
Django application.

The ``TWILIO_ACCOUNT_SID`` and ``TWILIO_AUTH_TOKEN`` variables can be found by
logging into your `Twilio account dashboard
<https://www.twilio.com/user/account>`_. These tokens are used to communicate
with the Twilio API, so be sure to keep these credentials safe!

The order in which Django will check for credentials is:

    1. Environment variables in your environment
    2. Settings variables in the Django settings

We recommend using environment variables so you can keep secret tokens out
of your code base.  This practice is far more secure.

Using ``virtualenv``, open up your ``/bin/activate.sh`` file and add the
following to the end::

    export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXX
    export TWILIO_AUTH_TOKEN=YYYYYYYYYYYY

You'll need to deactivate and restart your virtualenv for it to take effect.

To use settings variables, you'll need to add them to your ``settings.py``
file::

    TWILIO_ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    TWILIO_AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

.. note::
    Storing tokens in ``settings.py`` is very bad for security! Only do this
    if you are certain you will not be sharing the file publicly.

And optionally add the default caller::

    TWILIO_DEFAULT_CALLERID = 'NNNNNNNNNN'

If you specify a value for ``TWILIO_DEFAULT_CALLERID``, then all SMS and voice
messages sent through ``django-twilio`` functions will use the default caller id
as a convenience.

You can create a Credential object to store your variables if you want to use
multiple Twilio accounts or provide your users with Twilio compatibility.

When you want to use the credentials in a Credential object you need to manually
build a ``twilio.rest.Client`` like so::

    from twilio.rest import Client
    from django_twilio.utils import discover_twilio_credentials

    from django.contrib.auth.models import User

    my_user = User.objects.get(pk=USER_ID)

    account_sid, auth_token = discover_twilio_credentials(my_user)

    # Here we'll build a new Twilio_client with different credentials
    twilio_client = Client(account_sid, auth_token)
