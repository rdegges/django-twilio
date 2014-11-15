# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('django_twilio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwoFactorAuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('second_name', models.CharField(max_length=255, verbose_name='Second name')),
                ('username', models.CharField(max_length=255, verbose_name='Username')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(unique=True, max_length=128, verbose_name='Phone number')),
                ('two_factor_auth_code', models.IntegerField(max_length=4, blank=True)),
                ('two_factor_auth_id', models.CharField(max_length=255, blank=True)),
                ('verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
