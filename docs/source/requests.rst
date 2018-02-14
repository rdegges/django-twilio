Requests
==========

Django-twilio ships with some functionality to help handle inbound HTTP requests from Twilio. Sometimes it is confusing to understand what Twilio will send to your view endpoints, so these tools are designed to make that more explicit and easier to understand.

decompose()
-----------

The ``decompose`` function will strip out the Twilio-specific POST parameters from a Django HttpRequest object and present them back as a TwilioRequest object. Each POST parameter will be an attribute on the new TwilioRequest class. This makes it much easier to discover the parameters sent to you from Twilio and access them without having to use the HttpRequest object. The ``decompose`` function can also discover the type of Twilio request (''Message'' or ''Voice'') based on the parameters that are sent to you. This means you could build a single view endpoint and route traffic based on the type of Twilio request you receive!


Example usage
-------------

Here is an example::

    from twilio.twiml.messaging_response import MessagingResponse
    from django_twilio.decorators import twilio_view
    # include decompose in your views.py
    from django_twilio.request import decompose

    @twilio_view
    def inbound_view(request):

        response = MessagingResponse()

        # Create a new TwilioRequest object
        twilio_request = decompose(request)

        # See the Twilio attributes on the class
        twilio_request.to
        # >>> '+44123456789'

        # Discover the type of request
        if twilio_request.type is 'message':
            response.message('Thanks for the message!')
            return response

        # Handle different types of requests in a single view
        if twilio_request.type is 'voice':
            return voice_view(request)

        return response
