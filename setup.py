# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup

setup(

    # Basic package information:
    name='django-twilio',
    version='0.14.3.4-a1',
    packages=find_packages(),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,

    python_requires='>=3.10',
    # Package dependencies:
    install_requires=[
        'setuptools>=36.2',
        'twilio>=7',
        'Django>=4.2,<7',
        'django-phonenumber-field[phonenumbers]>=8.4.0',
        'phonenumbers>=8.10.22',
    ],

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
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ]

)
