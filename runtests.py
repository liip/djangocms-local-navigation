#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

from tests import settings as test_settings


def main():
    settings.configure(**{
        setting: getattr(test_settings, setting)
        for setting in dir(test_settings)
        if setting.isupper()
    })

    django.setup()
    test_runner = DiscoverRunner(verbosity=1)

    failures = test_runner.run_tests(['tests'])
    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    main()
