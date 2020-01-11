# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup
import sys


INSTALL_PYTHON_REQUIRES = []
if sys.version_info[0] == 2:
    # less than py3.4 can run 1.11-<2
    django_python_version_install = 'Django>=1.11,<2',
    INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
elif sys.version_info[0] == 3:
    if sys.version_info[1] == 4:
        # py3.4 can run 1.11-<2.1
        django_python_version_install = 'Django>=1.11,<2.1',
        INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
    elif 5 <= sys.version_info[1] < 7:
        # py3.5+ can run 1.11.17 < 2.2
        django_python_version_install = 'Django>=1.11,<3.0',
        INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
    elif sys.version_info[1] >= 7:
        django_python_version_install = 'Django>=1.11.17,<3.0'
        INSTALL_PYTHON_REQUIRES.append(django_python_version_install)
setup(

    # Basic package information:
    name='django-twilio',
    version='0.12.0rc1',
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
    license='UNLICENSE',
    url='https://github.com/rdegges/django-twilio',
    keywords='twilio telephony call phone voip sms django django-twilio',
    description='Build Twilio functionality into your Django apps.',
    long_description=open(
        normpath(join(dirname(abspath(__file__)), 'README.rst'))
    ).read(),
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ]

)
