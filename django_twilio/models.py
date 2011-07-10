from django.db import models


class Caller(models.Model):
    """A caller is defined uniquely by their phone number.

    :param bool blacklisted: Desginates whether the caller can use our
        services.
    :param char phone_number: Unique phone number in `E.164
        <http://en.wikipedia.org/wiki/E.164>`_ format.
    """
    blacklisted = models.BooleanField()
    phone_number = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.phone_number + (' (blacklisted) ' if self.blacklisted else '')
