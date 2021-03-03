#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:07
# software: PyCharm
# project: lingzhi-engine

from lingzhi_engine import const
from lingzhi_engine.base import R
from vuln.base.method_pool import AnonymousAndUserEndPoint
from vuln.models.vul_rule import IastVulRule
from vuln.serializers.vul_rule import VulRuleSerializer


class VulRuleEndPoint(AnonymousAndUserEndPoint):
    def get(self, request):
        user = request.user
        rule_type = request.query_params.get('type', 'system')

        if rule_type == const.RULE_USER and user.is_active is False:
            return R.success(status=202, msg='请先登录')

        if rule_type == const.RULE_USER:
            queryset = IastVulRule.objects.filter(create_by=user.id, is_enable=const.RULE_IS_ENABLE)
        elif rule_type == const.RULE_SYSTEM:
            queryset = IastVulRule.objects.filter(is_system=const.RULE_IS_SYSTEM, is_enable=const.RULE_IS_ENABLE)
        else:
            return R.success(status=203, msg='策略类型只能为user或system')

        data = VulRuleSerializer(queryset, many=True).data
        return R.success(data=data)
