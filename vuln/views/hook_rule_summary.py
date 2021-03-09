#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/9 下午12:06
# software: PyCharm
# project: lingzhi-engine
from lingzhi_engine import const
from lingzhi_engine.base import R
from vuln.base.method_pool import UserEndPoint
from vuln.models.hook_strategy import HookStrategy
from vuln.models.hook_type import HookType


class HookRuleSummaryEndPoint(UserEndPoint):
    def get(self, request):
        rule_type_queryset = HookType.objects.filter(enable=const.ENABLE,
                                                     created_by__in=[request.user, id, const.SYSTEM_USER_ID])
        rule_type_count = rule_type_queryset.count()

        sink_type_queryset = rule_type_queryset.filter(type=const.RULE_SINK)
        sink_count = HookStrategy.objects.filter(type__in=sink_type_queryset)

        rule_queryset = HookStrategy.objects.filter(type__in=rule_type_queryset)
        rule_count = rule_queryset.count()
        return R.success(data={
            'typeCount': rule_type_count,
            'ruleCount': rule_count,
            'sinkCount': sink_count
        })
