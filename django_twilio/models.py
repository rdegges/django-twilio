# -*- coding: utf-8 -*-

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Caller(models.Model):
    """A caller is defined uniquely by their phone number.

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
