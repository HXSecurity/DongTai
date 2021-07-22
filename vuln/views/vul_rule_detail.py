#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:07
# software: PyCharm
# project: lingzhi-engine
from django.db.models import Q
from dongtai.models.vul_rule import IastVulRule

from dongtai.utils import const
from dongtai.endpoint import R, AnonymousAndUserEndPoint
from vuln.serializers.vul_rule import VulRuleDetailSerializer


class VulRuleDetailEndPoint(AnonymousAndUserEndPoint):
    def get(self, request):
        rule_id = request.query_params.get('rule_id')
        if rule_id is None:
            return R.failure(msg='策略ID不能为空')

        user = request.user
        if user.is_active:
            queryset = IastVulRule.objects.filter(Q(is_system=const.RULE_IS_SYSTEM) | Q(create_by=user.id),
                                                  id=rule_id).first()
        else:
            queryset = IastVulRule.objects.filter(is_system=const.RULE_IS_SYSTEM, id=rule_id).first()
        if queryset:
            data = VulRuleDetailSerializer(queryset).data
            return R.success(data=data)
        else:
            return R.success(status=202, msg='查询失败')
