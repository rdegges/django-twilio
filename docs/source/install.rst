Installation
============

Installing django-twilio is simple.

Firstly, download and install django-twilio.

The easiest way is with `pip
<http://www.pip-installer.org/en/latest/>`_ ::

    $ pip install django-twilio


Requirements
------------

Django-twilio will automatically install the official `twilio-python library
<https://github.com/twilio/twilio-python>`_, which (other than Django), is the
only requirement.

The twilio-python library helps you rapidly build twilio applications, and it
is heavily suggested that you check out that project before using
django-twilio.


Django Integration
------------------

After django-twilio is installed, add it to your ``INSTALLED_APPS`` tuple in
your settings.py file::

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

Databases for Django 1.6 or lower
---------------------------------

To use django-twilio with Django 1.6.* or less, you will need to install `South <http://south.aeracode.org/docs/>`_ with the following terminal command::

    $ pip install South

Add south to your installed apps::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'django_twilio',
        'South'
        ...
    )

and run the default ```syncdb``` command::

    $ python manage.py syncdb

To sync the django-twilio models to the database run::

    $ python manage.py migrate django_twilio


Databases for Django 1.7
------------------------

Django 1.7 has built in migrations, so there is no need to install any third-party schema management tool. To sync the django-twilio models with your Django 1.7 project just run::

    $

Upgrading
---------

Upgrading django-twilio gracefully is easy using pip::

    $ pip install --upgrade django-twilio

Then you just need to update the models::

    $ python manage.py migrate django_twilio


Authentication Token Management
-------------------------------

Django-twilio offers multiple ways to add your Twilio credentials to your
Django application.

The ``TWILIO_ACCOUNT_SID`` and ``TWILIO_AUTH_TOKEN`` variables can be found by
logging into your `twilio account dashboard
<https://www.twilio.com/user/account>`_. These tokens are used to communicate
with the twilio API, be sure to keep these credentials safe!

The order in which Django will check for credentials is:

    1. Environment variables in your environment
    3. Settings variables in the Django settings

We recommend you use environment variables as these keep secret tokens out
of your code base (and therefore they're far more secure).

Using virtualenv open up your /bin/activate.sh file and add the following to the
end::

    export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXX
    export TWILO_AUTH_TOKEN=YYYYYYYYYYYY

You'll need to deactivate and restart your virtualenv for it to take effect.

To use settings variables, you'll need to add them to your settings.py file::

    TWILIO_ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    TWILIO_AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

.. note::
    Storing tokens in your settings.py is bad security! Only do this if you are certain you will not be sharing the file publicly.

And optionally add the default caller::

    TWILIO_DEFAULT_CALLERID = 'NNNNNNNNNN'

If you specify a value for ``TWILIO_DEFAULT_CALLERID``, than all SMS and voice
messages sent through django-twilio's functions will use the default caller id
as a convenience.

You can create a Credential object to store your variables if you want to use
multiple Twilio accounts or provide your users with Twilio compatibility.

When you want to use the credentials in a Credential object you need to manually
build a TwilioRestClient like so::

    from twilio.rest import TwilioRestClient
    from django_twilio.utils import discover_twilio_creds

    from django.contrib.auth.models import User

    myUser = User.objects.get(pk=USER_ID)

    creds = discover_twilio_creds(myUser)

    # Here we'll build a new twilio_client with different credentials
    twilio_client = TwilioRestClient(creds[0], creds[1])
