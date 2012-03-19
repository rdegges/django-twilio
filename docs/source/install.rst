Installation
============

Installing django-twilio is simple... Firstly, download and install
django-twilio. The easiest way is with `pip
<http://www.pip-installer.org/en/latest/>`_ ::

    pip install django-twilio


Requirements
------------

django-twilio will automatically install the official `twilio python library
<https://github.com/twilio/twilio-python>`_, which (other than Django), is the
only requirement.

The twilio python library helps you rapidly build twilio applications, and it
is heavily suggested that you check out that project before using
django-twilio.


Django Integration
------------------

After django-twilio is installed, add it to your ``INSTALLED_APPS`` tuple in
your settings module::

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

Then you'll need to add a few additional variables to your settings module::

    TWILIO_ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    TWILIO_AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

And optionally::

    TWILIO_DEFAULT_CALLERID = 'NNNNNNNNNN'

The ``TWILIO_ACCOUNT_SID`` and ``TWILIO_AUTH_TOKEN`` variables can be found by
logging into your `twilio account dashboard
<https://www.twilio.com/user/account>`_. These tokens are used to communicate
with the twilio API, be sure to keep these credentials safe!

If you specify a value for ``TWILIO_DEFAULT_CALLERID``, than all SMS and voice
messages sent through django-twilio's functions will use the default caller id
as a convenience.

Finally, run::

    python manage.py syncdb

To sync (and update) django-twilio's database models.

.. note::
    We recommend using `South <http://south.aeracode.org/docs/>`_ for database
    migrations. Initial migrations have already been created for django-twilio
    in django_twilio/migrations/, so you only need to run ``python manage.py
    migrate django_twilio`` instead of ``syncdb``.


Upgrading
---------

Upgrading django-twilio gracefully is easy using South. If you aren't using
South, you're out of luck(!)::

    python manage.py migrate django_twilio
