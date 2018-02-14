Decorators
==========

One of the key features of ``django-twilio`` is making it easy to build Django
views that return TwiML instructions back to Twilio, without having to deal with
all the complex security issues.

All-In-One Decorator
--------------------

The most useful decorator that ships with ``django-twilio`` is ``twilio_view``,
which will make your life much easier.

The ``django_twilio.decorators.twilio_view`` decorator:

1. Protects your views against forgery, and ensures that the request which hits
   your view originated from Twilio's servers. This way, you don't have to
   worry about fake requests hitting your views that may cause you to launch
   calls, or waste any money on fraudulent activity.

2. Ensures your view is CSRF exempt. Since Twilio will always POST data to your
   views, you'd normally have to explicitly declare your view CSRF exempt. The
   decorator does this automatically.

3. Enforces a blacklist. If you've got any :class:`django_twilio.models.Caller`
   objects who are blacklisted, any service requests from them will be rejected.

   .. note::
      You can manage your blacklist via the Django admin panel (if you have it
      enabled). ``django-twilio`` provides a ``Caller`` admin hook that allows
      you to create new callers, and blacklist them if you wish.

4. Allows you to (optionally) return raw TwiML responses without building an
   ``HttpResponse`` object. This can save a lot of redundant typing.

Example usage
-------------

Let's take a look at an example::

    from twilio.twiml.messaging_response import MessagingResponse
    from django_twilio.decorators import twilio_view

    @twilio_view
    def reply_to_sms_messages(request):
        r = MessagingResponse()
        r.message('Thanks for the SMS message!')
        return r

In the example above, we built a view that Twilio can POST data to, and that
will instruct Twilio to send a SMS message back to the person who messaged us
saying, "Thanks for the SMS message!".


Class based view example
------------------------

Here's the same thing as above, using a class-based view::

    from twilio.twiml.messaging_response import MessagingResponse

    from django.views.generic import View
    from django.utils.decorators import method_decorator

    from django_twilio.decorators import twilio_view

    class ThanksView(View):

        @method_decorator(twilio_view)
        def dispatch(self, request, *args, **kwargs):
            return super(ResponseView, self).dispatch(request, *args, **kwargs)

        def post(self, request):
            r = MessagingResponse()
            r.message('Thanks for the SMS message!')
            return r


How Forgery Protection Works
----------------------------

Forgery protection is extremely important when writing Twilio code. Since your
code will be doing stuff that costs money (sending calls, SMS messages, etc.),
ensuring all incoming HTTP requests actually originate from Twilio is really
important.

The way ``django-twilio`` implements forgery protection is by checking for a
specific flag in the django configuration settings::

    DJANGO_TWILIO_FORGERY_PROTECTION = False

If this setting is not present, it will default to the **opposite** of
``settings.DEBUG``; in debug mode, forgery protection will be off.

This behavior has been specifically implemented this way so that, while in
development mode, you can:

* Unit test your Twilio views without getting permission denied errors.
* Test your views out locally and make sure they return the code you want.

Because of this, it is extremely important that when your site goes live, you
ensure that ``settings.DEBUG = False`` and ``DJANGO_TWILIO_FORGERY_PROTECTION = True``.
