Gotchas
=======

Below is a list (which is being continuously expanded) on things which may "get
you" at one point or another. We've done our best to try and make django-twilio
as easy to use as possible, but sometimes problems are unavoidable!

Help! I Get HTTP 403 Forbidden
------------------------------

There are two common problems that cause django-twilio to return HTTP 403 errors
in your views:

Forgery Protection
------------------

django-twilio has built in forgery protection to help verify that requests made
to any of your twilio views actually originate from twilio.

We do this by analyzing HTTP requests sent to your views and comparing a special
cryptographic hash. This way, attackers are not able to simply POST data to your
views and waste your twilio resources. Attacks of this nature can be expensive
and troublesome.

In the event that HTTP requests to your views are determined to be forged,
django-twilio will return an HTTP 403 (forbidden) response.

Because of the way this forgery protection works, you'll get HTTP 403 errors
when hitting django-twilio views if you test them yourself and you have
``settings.DEBUG = False``. If you'd like to test your views, be sure to do so
with Django's DEBUG setting ON.

Missing Settings
----------------

django-twilio *requires* that you specify the variables ``TWILIO_ACCOUNT_SID``
and ``TWILIO_AUTH_TOKEN`` in your site's settings module. These are used to
verify the legitimacy of HTTP requests to your twilio views.

If these variables are missing, django-twilio will raise HTTP 403 (forbidden)
errors since it is unable to determine whether or not the HTTP request
originated from twilio.

To fix this, simply add these variables into your site's settings module.
