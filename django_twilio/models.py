# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField


class Caller(models.Model):
    """ A caller is defined uniquely by their phone number.

    :param bool blacklisted: Designates whether the caller can use our
        services.
    :param char phone_number: Unique phone number in `E.164
        <http://en.wikipedia.org/wiki/E.164>`_ format.

    """
    blacklisted = models.BooleanField()
    phone_number = PhoneNumberField(unique=True)

    def __unicode__(self):
        name = str(self.phone_number)
        if self.blacklisted:
            name += ' (blacklisted)'
        return name


class Credential(models.Model):
    """ A Credential model is a set of SID / AUTH tokens for the Twilio.com API

        The Credential model can be used if a project uses more than one
        Twilio account, or provides Users with access to Twilio powered
        web apps that need their own custom credentials.

    :param char name: The name used to distinguish this credential
    :param char account_sid: The Twilio account_sid
    :param char auth_token: The Twilio auth_token
    :param key user: The user linked to this Credential

    """

    def __unicode__(self):
        return ' '.join([self.name, '-', self.account_sid])

    name = models.CharField(max_length=30)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    account_sid = models.CharField(max_length=34)

    auth_token = models.CharField(max_length=32)
