# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup
import sys


INSTALL_PYTHON_REQUIRES = []
# We are intending to keep up to date with the supported Django versions.
# For the official support, please visit:
# https://docs.djangoproject.com/en/3.2/faq/install/#what-python-version-can-i-use-with-django and you may change the version in the URL to suit your needs, and we will try to update that here too as we upgrade with django.
if sys.version_info[1] == 5:
    django_python_version_install = 'Django>=2.2,<3.0',
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 6:
    django_python_version_install = 'Django>=2.2,<3.3',
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 7:
    django_python_version_install = 'Django>=2.2,<3.3'
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 8:
    django_python_version_install = 'Django>=2.2.8,<3.3'
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 9:
    # slightly too broad (3.0.11 for v3.0, and 3.1.3 for v3.1) -- may need to fix
    django_python_version_install = 'Django>=2.2.17,<3.3'
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[1] == 10:
    django_python_version_install = 'Django>=3.2.9,<3.3'
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)

setup(

    # Basic package information:
    name='django-twilio',
    version='0.13.2.a2',
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
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ]

)
