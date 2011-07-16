from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup


setup(

    # Basic package information:
    name = 'django-twilio',
    version = '0.1',
    packages = find_packages(),

    # Packaging options:
    zip_safe = False,
    include_package_data = True,

    # Package dependencies:
    install_requires = ['twilio>=3.0.0'],
    tests_require = ['django-nose>=0.1.3', 'coverage>=3.5'],

    # Metadata for PyPI:
    author = 'Randall Degges',
    author_email = 'rdegges@gmail.com',
    license = 'UNLICENSE',
    url = 'http://twilio.com/',
    keywords = 'twilio telephony call phone voip sms',
    description = 'A simple library for building twilio-powered Django webapps.',
    long_description = open(normpath(join(dirname(abspath(__file__)), 'README'))).read()

)
