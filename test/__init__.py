#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/13 下午10:21
# project: dongtai-engine
import os
import unittest

import django


class DongTaiTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapi.settings")
        os.environ.setdefault("debug", "true")
        django.setup()
