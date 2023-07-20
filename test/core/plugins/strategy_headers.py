#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime: 2021/10/22 下午2:57

import unittest

from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_check_response_header(self):
        from dongtai_engine.plugins.strategy_headers import check_response_header
        from dongtai_common.models.agent_method_pool import MethodPool

        check_response_header(MethodPool.objects.first())

    def test_check_strict_transport_security(self):
        value = "max-age=31536000; includeSubDomains"
        import re

        result = re.match("max-age=(\\d+);.*?", value)
        if result:
            print(result.group(1))


if __name__ == "__main__":
    unittest.main()
