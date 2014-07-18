import sys

import django

from django.conf import settings

settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    ROOT_URLCONF="django_twilio.tests.urls",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "django_twilio",
    ],
    SITE_ID=1,
    NOSE_ARGS=['-s'],
    AUTH_USER_MODEL='auth.User',
    TWILIO_AUTH_TOKEN='ACXXXXXXXXXXXX',
    TWILIO_ACCOUNT_SID='SIXXXXXXXXXXXX',
)

from django_nose import NoseTestSuiteRunner

def run_tests(*test_args):

    django.setup()

    if not test_args:
        test_args = ['django_twilio/tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
