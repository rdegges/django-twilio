# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup
import sys


INSTALL_PYTHON_REQUIRES = []
# We are intending to keep up to date with the supported Django versions.
# For the official support, please visit:
# https://docs.djangoproject.com/en/3.0/faq/install/#what-python-version-can-i-use-with-django and you may change the version in the URL to suit your needs, and we will try to update that here too as we upgrade with django.
if sys.version_info[1] == 5:
    # py3.5 can run 1.11 < 2.2
    django_python_version_install = 'Django>=2.2,<3.0',
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 6:
    # py3.6 can run 1.11 < 3.1 (likely will be <4.0)
    django_python_version_install = 'Django>=2.2,<3.2',
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 7:
    # py3.7 is 1.11.17 < 3.1 (likely will be <4.0)
    django_python_version_install = 'Django>=2.2,<3.2'
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 8:
    # py3.8 is 2.2.8 < 3.1 (likely will be <4.0)
    django_python_version_install = 'Django>=2.2.8,<3.2'
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)

setup(

    # Basic package information:
    name='django-twilio',
    version='0.13.1.b2',
    packages=find_packages(),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,

    # Package dependencies:
    install_requires=[
        'setuptools>=36.2',
        'twilio>=6.3.0,<7',
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
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ]

)
