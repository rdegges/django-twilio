Decorators
==========

One of django-twilio's key features is making it easy to build twilio views for
your project, and avoid nasty boilerplate code. Let's take a look!


All-In-One Decorator
--------------------

The most useful decorator that ships with django-twilio is
:func:`django_twilio.decorators.twilio_view`, which will, in most cases,
provide enough functionality to make your life much easier.

The :func:`django_twilio.decorators.twilio_view` decorator:

1. Protects your views against forgery, and ensures that the request which hits
   your view originated from twilio's servers. This way, you don't have to
   worry about fake requests hitting your views that may cause you to launch
   calls, or waste any money on fradulent activity.

2. Ensures your view is CSRF exempt. Since twilio will always POST data to your
   views, you'd normally have to explicitly declare your view CSRF exempt.
   :func:`django_twilio.decorators.twilio_view` does this automatically.

3. Allows you to (optionally) return raw TwiML responses without building an
   `HttpResponse` object. This can save a lot of redundant typing.

Let's take a look at a few examples::

    from twilio import Response, Sms
    from django_twilio.decorators import twilio_view

    @twilio_view
    def reply_to_sms_messages(request):
        r = Response()
        r.append(Sms('Thanks for the SMS message!'))
        return r

In the example above, we built a view that twilio can POST data to, and that
will instruct twilio to send a SMS message back to the person who messaged us
saying "Thanks for the SMS message!".

Now let's take a look at the same view written *without*
:func:`django_twilio.decorators.twilio_view`::

    from twilio import Response, Sms
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_POST
    from django.http import HttpResponse

    @csrf_exempt
    @require_POST
    def reply_to_sms_messages(request):
        r = Response()
        r.append(Sms('Thanks for the SMS message!'))
        return HttpResponse(r, mimetype='text/xml')

And that doesn't even include the forgery protection! As you can see, it's
a lot simpler to just wrap your twilio views with the
:func:`django_twilio.decorators.twilio_view` decorator.
