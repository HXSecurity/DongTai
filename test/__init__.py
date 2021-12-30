#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/29 下午7:23
# project: dongtai-engine
import os
import unittest

import django


# from django.test import TestCase


class DongTaiTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lingzhi_engine.settings")
        os.environ.setdefault("debug", "true")
        django.setup()

    def test_a(self):
        print("this is DongTaiTestCase class")
