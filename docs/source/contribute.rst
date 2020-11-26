Contributing
============

``django-twilio`` is always under development, and welcomes any contributions!
If you'd like to get your hands dirty with the source code, please fork the
project on `our GitHub page <https://github.com/rdegges/django-twilio>`_.

The guidelines below should help you get started.


Setup
-----

1. Fork the project on Github
2. Create a separate, **well named** branch to work on, off of the **develop**
   branch.
3. Use the Makefile to set up your development environment::

    $ make install-test

You should now have the ``django-twilio`` source code and development
environment ready to go. Run the tests to ensure everything is okay::

    $ make test

The tests should return with no failures.

Style
-----

When contributing code, please try to keep the style matching that of the
codebase. Right now, that means:

* 100% `PEP-8 compliance <http://www.python.org/dev/peps/pep-0008/>`_.
* Proper spelling / punctuation in the source code.

After setting up your development environment, you can run::

    $ make lint

This will lint the entire project and ensure PEP8 standards are being stuck to.

**Please note**: We're pretty relaxed on line length, but make sure you keep
it below 90 characters where possible.


Docs
----

If you'd like to contribute any documentation, just dig right in! There are
tons of things that can be improved, so don't feel shy! We use `Sphinx
<http://sphinx.pocoo.org/>`_ to build our documentation, and we host our
documentation online at `ReadTheDocs <http://readthedocs.org/>`_.


Tests
-----

In order to ensure high-quality releases, ``django-twilio`` aims to have an
extensive test suite. All test suite patches and additions are welcome, and
encouraged for new developers! The tests are well documented, and can be
a great way to introduce yourself to the codebase!

To run the tests, you can either use::

    $ make test

You'll see output that looks something like::

    nosetests --with-coverage --cover-package=django_twilio --verbosity=1
    Creating test database for alias 'default'...
    ......................................
    Name                                          Stmts   Miss  Cover   Missing
    ---------------------------------------------------------------------------
    django_twilio                                     2      0   100%
    django_twilio.client                              4      0   100%
    django_twilio.decorators                         50      4    92%   74-75, 103-104
    django_twilio.migrations                          0      0   100%
    django_twilio.models                             20      0   100%
    django_twilio.settings                            3      0   100%
    django_twilio.utils                              30      2    93%   44, 49
    django_twilio.views                              38      0   100%
    ---------------------------------------------------------------------------
    TOTAL                                           161      8    95%
    ----------------------------------------------------------------------
    Ran 38 tests in 0.184s

    OK
    Destroying test database for alias 'default'...

That's it! As you can see, when you run the test suite, ``django-twilio`` should
output not only failing test results, but also the coverage reports.

When you submit patches or add functionality to ``django-twilio``, be sure to
run the test suite to ensure that no functionality is broken!

Workflow
--------

When contributing to ``django-twilio``, here's a typical developer workflow::

    # Preparing the environment:

    $ git clone https://github.com/<your_username>/django-twilio.git
    $ cd django_twilio/
    $ git remote add upstream https://github.com/rdegges/django-twilio.git
    $ git checkout develop
    $ git pull upstream develop
    $ make install-test

    # Hacking:

    $ git checkout develop
    $ vim ...
    <<< hack time >>>

    # Writing tests:

    $ cd test_project/test_app/
    $ vim ...
    <<< hack time >>>

    # Running tests:

    $ cd django_twilio/
    $ make test
    <<< check test output >>>

.. note::
    Please be sure that if you fork the project, you work on the ``develop``
    branch. When submitting pull requests, please do so only if they're for the
    ``develop`` branch.


Bugs / Feature Requests / Comments
----------------------------------

If you've got any concerns about ``django-twilio``, make your voice heard by
posting an issue on our `GitHub issue tracker
<https://github.com/rdegges/django-twilio/issues>`_. All bugs / feature
requests / comments are welcome.
