# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Caller(models.Model):
    """
    A caller is defined uniquely by their phone number.

    :param bool blacklisted: Designates whether the caller can use our
        services.
    :param char phone_number: Unique phone number in `E.164
        <http://en.wikipedia.org/wiki/E.164>`_ format.

    """
    blacklisted = models.BooleanField(default=False)
    phone_number = PhoneNumberField(unique=True)

    def __str__(self):
        return '{phone_number}{blacklist_status}'.format(
            phone_number=str(self.phone_number),
            blacklist_status=' (blacklisted)' if self.blacklisted else '',
        )

    class Meta:
        app_label = 'django_twilio'


class Credential(models.Model):
    """
    A Credential model is a set of SID / AUTH tokens for the Twilio.com API

        The Credential model can be used if a project uses more than one
        Twilio account, or provides Users with access to Twilio powered
        web apps that need their own custom credentials.

    :param char name: The name used to distinguish this credential
    :param char account_sid: The Twilio account_sid
    :param char auth_token: The Twilio auth_token
    :param key user: The user linked to this Credential

    """

    def __str__(self):
        return '{name} - {sid}'.format(name=self.name, sid=self.account_sid)

    name = models.CharField(max_length=30)

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)

    account_sid = models.CharField(max_length=34)

    auth_token = models.CharField(max_length=32)

    class Meta:
        app_label = 'django_twilio'
