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

* Tabs instead of spaces.
* 4 spaces = 1 tab.
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


Bugs / Feature Requests / Comments
----------------------------------

If you've got any concerns about django-twilio, make your voice heard by
posting an issue on our `GitHub issue tracker
<https://github.com/rdegges/django-twilio/issues>`_. All bugs / feature
requests / comments are welcome.


TODO
----

Below is the current list of features that are planned. If you'd like to help
write them or get involved, fork the project and send a pull request.

.. note::
    django-twilio aims to be really well-tested. So when submitting features
    / patches for code, including tests will help patches be implemented
    quicker.

* Data models for tracking SMS messages and Voice messages.
* Optional `log` keyword argument for the
  :func:`django_twilio.decorators.twilio_view` decorator. This will force
  django-twilio to log all requests from twilio to the database.
* Blacklist capabilities and related admin panel hooks. The blacklist
  functionality will allow admins to blacklist certain numbers that may be
  abusing services (people who place repeated calls, etc.).
