#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午7:54
# software: PyCharm
# project: lingzhi-engine
from lingzhi_engine.base import R
from vuln.base.method_pool import AnonymousAndUserEndPoint


class VulRuleTypeEndPoint(AnonymousAndUserEndPoint):
    def get(self, request):
        results = [{'label': '污点源方法', 'value': 'sources'}, {'label': '传播方法', 'value': 'propagators'},
                   {'label': '危险方法', 'value': 'sinks'}]
        return R.success(data=results)
