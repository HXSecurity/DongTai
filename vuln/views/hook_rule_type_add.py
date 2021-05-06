#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/9 下午12:06
# software: PyCharm
# project: lingzhi-engine
import json
import time

from dongtai_models.models.hook_talent_strategy import IastHookTalentStrategy
from dongtai_models.models.hook_type import HookType

from lingzhi_engine import const
from lingzhi_engine.base import R
from vuln.base.method_pool import UserEndPoint


class HookRuleTypeAddEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_type = request.data.get('type')
            rule_type = int(rule_type)
            if rule_type not in (
                    const.RULE_SOURCE, const.RULE_ENTRY_POINT, const.RULE_PROPAGATOR, const.RULE_FILTER,
                    const.RULE_SINK):
                rule_type = None

            name = request.data.get('name')

            short_name = request.data.get('short_name')

            enable = request.data.get('enable')
            enable = int(enable)
            if enable not in (const.ENABLE, const.DISABLE):
                return None, None, None, None
            return rule_type, name, short_name, enable
        except Exception as e:
            # todo 增加异场打印
            return None, None, None, None

    def post(self, request):
        rule_type, name, short_name, enable = self.parse_args(request)
        if all((rule_type, name, short_name)) is False:
            return R.failure(msg='数据不完整')
        timestamp = int(time.time())
        hook_type = HookType(enable=enable, type=rule_type, name=short_name, value=name, create_time=timestamp,
                             update_time=timestamp, created_by=request.user.id)
        hook_type.save()
        # 将hook规则添加至策略集中
        talent = request.user.get_talent()
        if talent:
            talent_rule = IastHookTalentStrategy.objects.filter(talent=talent).first()
            if talent_rule:
                rule_types = json.loads(talent_rule.values)
                rule_types.append(hook_type.id)
                talent_rule.values = json.dumps(rule_types)
                talent_rule.save()
        return R.success(msg='规则类型保存成功')
