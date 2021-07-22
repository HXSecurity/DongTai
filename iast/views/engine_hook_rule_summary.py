#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:59
# software: PyCharm
# project: lingzhi-webapi
from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from dongtai.utils import const


class EngineHookRuleSummaryEndPoint(UserEndPoint):
    def get(self, request):
        rule_type_queryset = HookType.objects.filter(created_by__in=[request.user.id, const.SYSTEM_USER_ID])
        rule_type_count = rule_type_queryset.values('id').count()

        sink_type_queryset = rule_type_queryset.filter(type=const.RULE_SINK)
        sink_count = HookStrategy.objects.values('id').filter(type__in=sink_type_queryset).count()

        rule_count = HookStrategy.objects.values('id').filter(type__in=rule_type_queryset).count()
        return R.success(data={
            'typeCount': rule_type_count,
            'ruleCount': rule_count,
            'sinkCount': sink_count
        })
