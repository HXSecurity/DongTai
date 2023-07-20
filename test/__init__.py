#!/usr/bin/env python
# datetime: 2021/7/13 下午10:21
from django.test.runner import DiscoverRunner
from django.core.cache import cache
import os
import unittest
import django


class DongTaiTestCase(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dongtai_conf.settings")
        os.environ.setdefault("debug", "true")
        cache.clear()
        django.setup()


class NoDbTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
