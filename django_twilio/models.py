from django.db import models


class Caller(models.Model):
	"""A caller is defined uniquely by their phone number."""
	blacklisted = models.BooleanField()
	phone_number = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.phone_number + (' (blacklisted) ' if self.blacklisted else '')
