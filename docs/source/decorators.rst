Decorators
==========

One of django-twilio's key features is making it easy to build twilio views for
your project, and avoid nasty boilerplate code. Let's take a look!


All-In-One Decorator
--------------------

The most useful decorator that ships with django-twilio is
:func:`django_twilio.decorators.twilio_view`, which will make your life much
easier.

The :func:`django_twilio.decorators.twilio_view` decorator:

1. Protects your views against forgery, and ensures that the request which hits
   your view originated from twilio's servers. This way, you don't have to
   worry about fake requests hitting your views that may cause you to launch
   calls, or waste any money on fradulent activity.

2. Ensures your view is CSRF exempt. Since twilio will always POST data to your
   views, you'd normally have to explicitly declare your view CSRF exempt.
   :func:`django_twilio.decorators.twilio_view` does this automatically.

3. Enforces a blacklist. If you've got any
   :class:`django_twilio.models.Caller` objects who are blacklisted, any
   service requests from them will be rejected.

   .. note::
      You can manage your blacklist via the Django admin panel (if you have it
      enabled). django-twilio provides a ``Caller`` admin hook that allows you
      to create new callers, and blacklist them if you wish.

4. Allows you to (optionally) return raw TwiML responses without building an
   ``HttpResponse`` object. This can save a lot of redundant typing.

Let's take a look at a few examples::

    from twilio.twiml import Response
    from django_twilio.decorators import twilio_view

    @twilio_view
    def reply_to_sms_messages(request):
        r = Response()
        r.sms('Thanks for the SMS message!')
        return r

In the example above, we built a view that twilio can POST data to, and that
will instruct twilio to send a SMS message back to the person who messaged us
saying "Thanks for the SMS message!".

Now let's take a look at the same view written *without*
:func:`django_twilio.decorators.twilio_view`::

    from twilio.twiml import Response
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_POST
    from django.http import HttpResponse

    @csrf_exempt
    @require_POST
    def reply_to_sms_messages(request):
        r = Response()
        r.sms('Thanks for the SMS message!')
        return HttpResponse(r.__repr__(), mimetype='application/xml')

And that doesn't even include forgery protection or blacklist management! As
you can see, using the :func:`django_twilio.decorators.twilio_view` decorator
can save you a lot of time.


How Forgery Protection Works
****************************

Forgery protection is extremely important when writing Twilio code. Since your
code will be doing stuff that costs money (sending calls, SMS messages,
etc.), ensuring all incoming HTTP requests actually originate from Twilio is
really important.

The way django-twilio implements forgery protection is by *only* enabling it
when ``settings.DEBUG = False``--thereby only doing the validation checks when
your site is running in production.

This behavior has been specifically implemented this way so that, while in
development mode, you can:

* Unit test your Twilio views without getting permission denied errors.
* Test your views out locally and make sure they return the code you want.

Because of this, it is extremely important that when your site goes live, you
ensure that ``settings.DEBUG = False``!!! **If you have**
``settings.DEBUG = True`` **enabled, bad things will happen!**
