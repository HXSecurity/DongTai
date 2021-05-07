#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/9 下午12:06
# software: PyCharm
# project: lingzhi-engine
from dongtai_models.models.hook_strategy import HookStrategy

from lingzhi_engine import const
from lingzhi_engine.base import R, UserEndPoint


class HookRuleDeleteEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_id = request.query_params.get('rule_id', const.RULE_PROPAGATOR)
            rule_type = int(rule_id)
            return rule_type
        except Exception as e:
            # todo 增加异常打印
            return None

    def get(self, request):
        rule_id = self.parse_args(request)
        if rule_id is None:
            return R.failure(msg='策略不存在')

        rule = HookStrategy.objects.filter(id=rule_id, created_by=request.user.id).first()
        if rule:
            rule.enable = const.DELETE
            rule.save()
            return R.success(msg='删除成功')
        else:
            return R.failure(msg='策略不存在')
