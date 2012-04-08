# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Caller'
        db.create_table('django_twilio_caller', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blacklisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('django_twilio', ['Caller'])

    def backwards(self, orm):
        # Deleting model 'Caller'
        db.delete_table('django_twilio_caller')

    models = {
        'django_twilio.caller': {
            'Meta': {'object_name': 'Caller'},
            'blacklisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['django_twilio']