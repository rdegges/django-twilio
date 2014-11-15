# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
This module provides useful django admin hooks that allow you to manage
various components through the django admin panel (if enabled).
"""

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (
    Caller,
    Credential,
    TwoFactorAuthUser
)


class CallerAdmin(admin.ModelAdmin):
    """This class provides admin panel integration for our
    :class:`django_twilio.models.Caller` model.
    """
    list_display = ('__str__', 'blacklisted')


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new TwoFactorAuthUser users.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        class = TwoFactorAuthUser
        fields = (
            'first_name', 'second_name', 'email', 'username', 'phone_number')

        help_texts = {
            'phone_number' : 'The phone number of this user.'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """
    A form for updating TwoFactorAuthUser users.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        class = TwoFactorAuthUser
        fields = (
            'first_name', 'second_name', 'email', 'username', 'phone_number')

        help_texts = {
            'phone_number' : 'The phone number of this user.'
        }

    def clean_password(self):
        return self.initial['password']


def TwoFactorAuthUserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username', 'email', 'first_name', 'second_name', 'phone_number',
        'verified', 'two_factor_auth_code', 'two_factor_auth_id',
        'is_active', 'is_admin')

    list_filter = ('verified', 'is_active', 'is_admin')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('username', 'first_name', 'second_name',)
        }),
        ('Two Factor Authentication',
            {'fields': (
                'phone_number', 'two_factor_auth_code', 'two_factor_auth_id',
                'verified')
            }),
        ('Permissions', {'fields': ('is_active', 'is_admin',)}),
    )

    search_fields = ('email', 'username', 'first_name', 'second_name')



admin.site.register(Caller, CallerAdmin)
admin.site.register(Credential)
admin.site.unregister(Group)
admin.site.register(TwoFactorAuthUser, TwoFactorAuthUserAdmin)
