from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup


setup(

    # Basic package information:
    name = 'django-twilio',
    version = '0.5.1',
    packages = find_packages(),

    # Packaging options:
    zip_safe = False,
    include_package_data = True,

    # Package dependencies:
    install_requires = ['twilio>=3.3.6', 'Django>=1.3.1', 'django-phonenumber-field>=0.2a3'],

    # Metadata for PyPI:
    author = 'Randall Degges',
    author_email = 'rdegges@gmail.com',
    license = 'UNLICENSE',
    url = 'http://twilio.com/',
    keywords = 'twilio telephony call phone voip sms',
    description = 'Build Twilio functionality into your Django apps.',
    long_description = open(normpath(join(dirname(abspath(__file__)),
        'README.rst'))).read()

)
