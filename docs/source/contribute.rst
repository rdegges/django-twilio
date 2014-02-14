Contributing
============

django-twilio is always under development, and welcomes any contributions!
If you'd like to get your hands dirty with the source code, please fork the
project on `our GitHub page <https://github.com/rdegges/django-twilio>`_.

The guidelines below should help you get started.


Style
-----

When contributing code, please try to keep the style matching that of the
codebase. Right now, that means:

* 100% `PEP-8 compliance <http://www.python.org/dev/peps/pep-0008/>`_.
* Proper spelling / punctuation in the source code.

After setting up your developer environment you can run::

    $ flake8 django_twilio

This will lint the entire project and ensure PEP8 standards are being stuck to.

**Please note**: We're pretty relaxed on line length, but make sure you keep
it below 90 charactes where possible.


Docs
----

If you'd like to contribute any documentation, just dig right in! There are
tons of things that can be improved, so don't feel shy! We use `Sphinx
<http://sphinx.pocoo.org/>`_ to build our documentation, and we host our
documentation online at `ReadTheDocs <http://readthedocs.org/>`_.


Tests
-----

In order to ensure high-quality releases, django-twilio aims to have an
extensive test suite. All test suite patches and additions are welcome, and
encouraged for new developers! The tests are well documented, and can be
a great way to introduce yourself to the codebase!

To run the tests, you'll need to do the following:

1. Check out the latest version of django-twilio's source code using git:
   ``git clone git://github.com/rdegges/django-twilio.git``.

2. Switch to the develop branch: ``cd django-twilio; git fetch origin
   develop:develop``.

3. Install the required packages for testing: ``pip install -r requirements.txt``.

4. Install django-twilio in development mode: ``python
   setup.py develop``.

5. Before running these tests, you need to set up some environment variables.
   If you're using virtualenv, open the */bin/activate* file in vi or nano and
   add the following to the end::

    export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXXX
    export TWILIO_AUTH_TOKEN=YYYYYYYYYYYYYYY

Obviously you'll need to replace this with your own account details.

.. note::

    The test suite will not cost you any credit from your Twilio account.

6. Run the test suite using the run_tests.py command like so::

    $ python run_tests.py

You'll see output that looks something like::

    Creating test database for alias 'default'...
    ..............................
    ------------------------------
    Ran 30 tests in 0.071s

    OK
    Destroying test database for alias 'default'...

That's it! As you can see, when you run the test suite, django-twilio should
output not only failing test results, but also the coverage reports.

When you submit patches or add functionality to django-twilio, be sure to run
the test suite to ensure that no functionality is broken.

Tests for Django 1.6.1
-----------------------

An alternative method of testing that works with Django 1.6.1 has been implemented.
(This is also how we run CI on django-twilio).



Make sure you replace your own tokens.

This testing method can be run using::

    $ python run_tests.py



Workflow
--------

When contributing to django-twilio, here's a typical developer workflow::

    # Preparing the environment:

    $ mkvirtualenv --no-site-packages djtw
    $ cd ~/django_twilio
    $ git checkout develop
    $ pip install -r requirements.txt
    $ python setup.py develop

    # Hacking:

    $ cd ~/django_twilio/django_twilio
    $ git checkout develop
    $ vim ...
    <<< hack >>>

    # Writing tests:

    $ cd ~/django_twilio/django_twilio/tests
    $ vim ...
    <<< hack >>>

    # Running tests:

    $ cd ~/django_twilio/test_project
    $ workon djtw
    $ python manage.py test django_twilio
    <<< check test output >>>

.. note::
    Please be sure that if you fork the project, you work on the ``develop``
    branch. When submitting pull requests, please do so only if they're for the
    ``develop`` branch.


Bugs / Feature Requests / Comments
----------------------------------

If you've got any concerns about django-twilio, make your voice heard by
posting an issue on our `GitHub issue tracker
<https://github.com/rdegges/django-twilio/issues>`_. All bugs / feature
requests / comments are welcome.
