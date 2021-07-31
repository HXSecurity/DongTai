#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/28 下午4:08
# project: dongtai-openapi
import os
import unittest

import django


class DongTaiTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgentServer.settings")
        os.environ.setdefault("debug", "true")
        django.setup()
