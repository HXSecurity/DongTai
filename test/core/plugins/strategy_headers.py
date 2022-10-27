#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/10/22 下午2:57
# project: DongTai-engine

import unittest

from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):

    def test_check_response_header(self) -> None:
        from dongtai_engine.plugins.strategy_headers import check_response_header
        from dongtai_common.models.agent_method_pool import MethodPool
        check_response_header(MethodPool.objects.first())

    def test_check_strict_transport_security(self) -> None:
        value = 'max-age=31536000; includeSubDomains'
        import re
        result = re.match('max-age=(\\d+);.*?', value)
        if result:
            print(result.group(1))


if __name__ == '__main__':
    unittest.main()
