#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:07
# software: PyCharm
# project: lingzhi-engine
import time

from lingzhi_engine.base import R
from vuln.base.method_pool import UserEndPoint
from vuln.models.vul_rule import IastVulRule


class VulRuleSaveEndPoint(UserEndPoint):
    """
    策略保存API，支持修改、新增
    """

    def post(self, request):
        rule_id = request.query_params.get('id')
        # todo 数据转换为json保存
        rule_name = request.data.get('id')
        rule_level = request.data.get('level')
        rule_msg = request.data.get('msg')
        rule_value = request.data
        is_system = True if request.user.is_system_admin() else False
        create_by = request.user.id
        timestamp = int(time.time())

        if rule_id:
            rule = IastVulRule.objects.filter(create_by=request.user.id, id=rule_id).first()
            rule.rule_value = rule_value
            rule.rule_name = rule_name
            rule.rule_level = rule_level
            rule.rule_msg = rule_msg
            rule.is_system = is_system
            rule.create_by = create_by
            rule.update_time = timestamp
        else:
            rule = IastVulRule(
                rule_name=rule_name,
                rule_level=rule_level,
                rule_msg=rule_msg,
                rule_value=rule_value,
                is_system=is_system,
                create_by=create_by,
                update_time=timestamp,
                create_time=timestamp
            )
        rule.save()

        return R.success(msg='规则保存成功')
