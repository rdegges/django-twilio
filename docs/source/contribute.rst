Contributing
============

django-twilio is still under development, and welcomes any code contributions!
If you'd like to get your hands dirty with the source code, please fork the
project on `our GitHub page <https://github.com/rdegges/django-twilio>`_.

The guidelines below should help you get started.


Style
-----

When contributing code, please try to keep the style matching that of the
codebase. Right now, that means:

* 100% `PEP-8 compliance <http://www.python.org/dev/peps/pep-0008/>`_.
* Proper spelling / punctuation in the source code.


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

4. Install django-twilio in development mode: ``cd django_twilio; python
   setup.py develop``.

5. Run the test suite using the test project that ships with django-twilio: ``cd
   ../test_project; python manage.py test django_twilio``.

You'll see output that looks something like::

    rdegges@lap:~/Code/rdegges/django-twilio/test_project$ workon django-twilio
    (django-twilio)rdegges@lap:~/Code/rdegges/django-twilio/test_project$ python manage.py test django_twilio
    nosetests --verbosity 1 django_twilio --with-coverage --cover-package=django_twilio
    Creating test database for alias 'default'...
    ......................
    Name                       Stmts   Miss  Cover   Missing
    --------------------------------------------------------
    django_twilio                  0      0   100%
    django_twilio.conf             3      0   100%
    django_twilio.decorators      34      0   100%
    django_twilio.models           6      0   100%
    django_twilio.views           29      0   100%
    --------------------------------------------------------
    TOTAL                         72      0   100%
    ----------------------------------------------------------------------
    Ran 22 tests in 1.184s

    OK
    Destroying test database for alias 'default'...

That's it! As you can see, when you run the test suite, django-twilio should
output not only failing test results, but also the coverage reports.

.. note::

    If you'd like to see more details about the tests that are ran, you can
    optionally specify the ``--verbosity=2`` flag on the command line, eg::

        python manage.py test django_twilio --verbosity=2

    This will increase the output level, and show detailed test run
    information.

.. note::
    I try to maintain 100% test coverage for django-twilio.

When you submit patches or add functionality to django-twilio, be sure to run
the test suite to ensure that no functionality is broken.

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
