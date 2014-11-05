# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup


setup(

    # Basic package information:
    name='django-twilio',
    version='0.8.0',
    packages=find_packages(),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,

    # Package dependencies:
    install_requires=[
        'twilio>=3.6.9',
        'Django>=1.4',
        'django-phonenumber-field>=0.6'
    ],

    # Metadata for PyPI:
    author='Randall Degges',
    author_email='rdegges@gmail.com',
    license='UNLICENSE',
    url='http://twilio.com/',
    keywords='twilio telephony call phone voip sms',
    description='Build Twilio functionality into your Django apps.',
    long_description=open(
        normpath(join(dirname(abspath(__file__)), 'README.rst'))
    ).read(),
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ]

)
