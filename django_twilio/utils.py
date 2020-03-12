# -*- coding: utf-8 -*-

from twilio.twiml.messaging_response import Message

from django_twilio.request import decompose

"""
Useful utility functions.
"""

import os

from django.http import HttpResponse
from django.conf import settings

from twilio.twiml.voice_response import VoiceResponse

from .models import Caller, Credential


def discover_twilio_credentials(user=None):
    """ Due to the multiple ways of providing SID / AUTH tokens through
        this package, this function will search in the various places that
        credentials might be stored.

        The order this is done in is:

        1. If a User is passed: the keys linked to the
           user model from the Credentials model in the database.
        2. Environment variables
        3. django.conf settings

        We recommend using environment variables were possible; it is the
        most secure option
    """

    SID = 'TWILIO_ACCOUNT_SID'
    AUTH = 'TWILIO_AUTH_TOKEN'

    if user:
        credentials = Credential.objects.filter(user=user.id)
        if credentials.exists():
            credentials = credentials[0]
            return credentials.account_sid, credentials.auth_token

    if SID in os.environ and AUTH in os.environ:
        return os.environ[SID], os.environ[AUTH]

    if hasattr(settings, SID) and hasattr(settings, AUTH):
        return settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN

    raise AttributeError(
        "Could not find {sid} or {auth} in environment variables, "
        "User credentials, or django project settings.".format(
            sid=SID,
            auth=AUTH,
        )
    )


def get_blacklisted_response(request):
    """Analyze the incoming Twilio request to determine whether or not to
    reject services. We'll only reject services if the user requesting service
    is on our blacklist.

    :param obj request: The Django HttpRequest object to analyze.
    :rtype: HttpResponse.
    :returns: HttpResponse if the user requesting services is blacklisted, None
        otherwise.
    """
    try:
        # get the `From` data from the request's payload.
        # Only supporting GET and POST.
        data = request.GET if request.method == 'GET' else request.POST
        frm = data['From']
        caller = Caller.objects.get(phone_number=frm)
        if caller.blacklisted:
            twilio_request = decompose(request)
            if twilio_request.type == 'voice':
                r = VoiceResponse()
                r.reject()
            else:
                # SMS does not allow to selectively reject SMS.
                # So, we respond with nothing, and twilio does not forward
                # the message back to the sender.
                r = Message()
            return HttpResponse(str(r), content_type='application/xml')
    except Exception:
        pass

    return None


def create_sub_account(user, twilio_client, friendly_name=None):
    new_account = twilio_client.api.accounts.create(friendly_name=friendly_name or user)
    new_credential = Credential.objects.create(user=user, account_sid=new_account.sid, auth_token=new_account.auth_token, name=new_account.friendly_name)
    return new_credential, new_account


def close_sub_account(account_sid, twilio_client):
    return twilio_client.accounts(account_sid).update(status="closed")


def close_sub_accounts_for_user(user, twilio_client):
    accounts = []
    for credential_obj in Credential.objects.filter(user=user):
        accounts.append(twilio_client.accounts(credential_obj.account_sid).update(status="closed"))
    return accounts


# Backwards compatibility for a poorly named function
discover_twilio_creds = discover_twilio_credentials
