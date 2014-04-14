#!/usr/bin/env python
import sys
from shutil import rmtree
from os.path import abspath, dirname, join

import django
from django.conf import settings


sys.path.insert(0, abspath(dirname(__file__)))


media_root = join(abspath(dirname(__file__)), 'test_files')
rmtree(media_root, ignore_errors=True)

installed_apps = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'simple_history',
    'simple_history.tests',
    'simple_history.tests.external',
)
auth_user_model = 'auth.User'
if django.VERSION >= (1, 5):
    installed_apps += ('simple_history.tests.custom_user', )
    auth_user_model = 'custom_user.CustomUser'

DEFAULT_SETTINGS = dict(
    ROOT_URLCONF='simple_history.tests.urls',
    MEDIA_ROOT=media_root,
    STATIC_URL='/static/',
    INSTALLED_APPS=installed_apps,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    AUTH_USER_MODEL=auth_user_model
)


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    if hasattr(django, 'setup'):
        django.setup()
    if django.VERSION < (1, 7): 
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner(verbosity=1, interactive=True, failfast=False).run_tests(['tests'])
        sys.exit(failures)
    else:
        from django.test.runner import DiscoverRunner
        failures = DiscoverRunner(
            pattern='test*.py', verbosity=1, interactive=True, failfast=False).run_tests(test_labels=None)
        sys.exit(failures)


if __name__ == "__main__":
    main()
