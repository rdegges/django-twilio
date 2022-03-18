# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup
import sys


INSTALL_PYTHON_REQUIRES = []
# We are intending to keep up to date with the supported Django versions.
# For the official support, please visit:
# https://docs.djangoproject.com/en/4.0/faq/install/#what-python-version-can-i-use-with-django
if sys.version_info[1] in [8, 9, 10]:
    django_python_version_install = "Django>=4.0,<4.1"
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)

setup(

    # Basic package information:
    name='django-twilio',
    version='0.14.0.a1',
    packages=find_packages(),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,

    # Package dependencies:
    install_requires=[
        'setuptools>=36.2',
        'twilio>=7,<8',
        'django-phonenumber-field>=0.6',
        'phonenumbers>=8.10.22',
    ] + INSTALL_PYTHON_REQUIRES,

    # Metadata for PyPI:
    author='Randall Degges',
    author_email='rdegges@gmail.com',
    maintainer="Jason Held",
    maintainer_email="jasonsheld@gmail.com",
    license='UNLICENSE',
    url='https://github.com/rdegges/django-twilio',
    keywords='twilio telephony call phone voip sms django django-twilio',
    description='Build Twilio functionality into your Django apps.',
    long_description=open(
        normpath(join(dirname(abspath(__file__)), 'README.rst'))
    ).read(),
    project_urls={
        "Documentation": "https://django-twilio.readthedocs.io/en/latest/",
        "Code": "https://github.com/rdegges/django-twilio",
        "Tracker": "https://github.com/rdegges/django-twilio/issues",
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ]

)
