# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)

from phonenumber_field.modelfields import PhoneNumberField

from .tfa_utils import (
    generate_two_factor_auth_details,
    send_two_factor_auth_message
)


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
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


@python_2_unicode_compatible
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

    user = models.OneToOneField(AUTH_USER_MODEL)

    account_sid = models.CharField(max_length=34)

    auth_token = models.CharField(max_length=32)


class TwoFactorAuthUserManager(BaseUserManager):
    """
    Manager for the TwoFactorAuthUser.
    """

    def do_two_fa_actions(self, user):
        """
        Handle all the two factor authentication actions
        """
        # Generate the codes we need for 2 Factor Authentication
        code, auth_id = generate_two_factor_auth_details()
        user.two_factor_auth_code = code
        user.two_factor_auth_id = auth_id

        # Send the user a 2 Factor Authentication sms message
        send_two_factor_auth_message(code, user.phone_number)

        return user

    def create_user(
        self, email, first_name, second_name, username, phone_number,
        password=None, is_admin=False):
        """
        Create a user and send an SMS message with a randomly generated
        code.
        """

        # Assert that we have all the required values
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not second_name:
            raise ValueError('Users must have a second name')
        if not username:
            raise ValueError('Users must have a username')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            second_name=second_name,
            username=username,
            phone_number=phone_number,
        )

        user.set_password(password)
        user = do_two_fa_actions(user)
        if is_admin:
            user.is_admin = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, second_name, username,
                         phone_number, password=None, is_admin=True):
        """
            Create a super user. Returns standard create_user function with
            is_admin = True
        """

        return create_user(email, first_name, second_name, username,
                           phone_number, password, is_admin)




@python_2_unicode_compatible
class TwoFactorAuthUser(AbstractBaseUser):
    """
    A TwoFactorAuthUser is a custom user model that implements Two factor
    authentication using SMS through Twilio. The TwoFactorAuthUser replaces
    the standard user.User model in Django and does not sublcass it.
    See the documentation on how to use the TwoFactorAuthUser.

    Attributes
    ----------

    email - the email address of the user.

    first_name - the first name of the user.

    second_name - the second name of the user.

    username - the username of the user.

    phone_number - The phone number of the user.

    two_factor_auth_code - A numbered code randomly generated when this user
                           is created.

    two_factor_auth_id - A randomly generated string that is created when this
                         user is created.

    verified - A boolean. False if user has not verified themselves. Default
               is false.

    """

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'email', 'first_name', 'second_name', 'phone_number', 'username'
    ]

    objects = TwoFactorAuthUserManager()

    def __str__(self):
        return '{0}, verified is {0}'.format(self.username, self.verified)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    first_name = models.CharField(
        verbose_name='First name',
        max_length=255
    )

    second_name = models.CharField(
        verbose_name='Second name',
        max_length=255
    )

    username = models.CharField(
        verbose_name='Username',
        max_length=255
    )

    phone_number = PhoneNumberField(
        verbose_name='Phone number',
        unique=True
    )

    two_factor_auth_code = models.IntegerField(max_length=4, blank=True)

    two_factor_auth_id = models.CharField(max_length=255, blank=True)

    verified = models.BooleanField(default=False, blank=True)

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)


    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.second_name)

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Not yet implemented
        return True

    def has_module_perms(self, app_label):
        # Not yet implemented
        return True

    @property
    def is_staff(self):
        return self.is_staff
