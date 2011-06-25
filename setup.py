from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup
from django_twilio import __version__ as version


setup(

	# Basic package information:
	name = 'django-twilio',
	version = version,
	packages = find_packages(),

	# Packaging options:
	zip_safe = False,
	include_package_data = True,

	# Package dependencies:
	install_requires = ['twilio>=2.0.10'],

	# Metadata for PyPI:
	author = 'Randall Degges',
	author_email = 'rdegges@gmail.com',
	license = 'UNLICENSE',
	url = 'http://twilio.com/',
	keywords = 'twilio telephony call phone voip sms',
	description = 'A simple library for building twilio-powered Django webapps.',
	long_description = open(normpath(join(dirname(abspath(__file__)), 'README'))).read()

)
