from __future__ import unicode_literals

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_app.settings'

from django.conf import settings
from django.test.utils import get_runner


def main():
    TestRunner = get_runner(settings)

    test_runner = TestRunner()

    failures = test_runner.run_tests(['test_app.tests'])

    sys.exit(failures)


if __name__ == '__main__':
    main()
