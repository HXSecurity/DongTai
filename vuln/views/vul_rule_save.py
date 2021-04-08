#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:07
# software: PyCharm
# project: lingzhi-engine
import json
import logging
import time

from lingzhi_engine.base import R
from vuln.base.method_pool import AnonymousAndUserEndPoint
from vuln.models.vul_rule import IastVulRule

logger = logging.getLogger('dongtai-engine')


class VulRuleSaveEndPoint(AnonymousAndUserEndPoint):
    """
    策略保存API，支持修改、新增
    """

    def parse_args(self, request):
        rule_id = request.query_params.get('id')
        rule_name = request.data.get('name')
        rule_level = request.data.get('level')
        rule_msg = request.data.get('msg')
        rule_value = json.dumps(request.data)
        is_system = True if request.user.is_system_admin() else False
        create_by = request.user.id
        timestamp = int(time.time())
        return rule_id, rule_name, rule_level, rule_msg, rule_value, is_system, create_by, timestamp

    @staticmethod
    def save_or_create_rule(**kwargs):
        try:
            if kwargs['rule_id']:
                rule = IastVulRule.objects.filter(create_by=kwargs['create_by'], id=kwargs['rule_id']).first()
                if rule:
                    rule.rule_value = kwargs['rule_value']
                    rule.rule_name = kwargs['rule_name']
                    rule.rule_level = kwargs['rule_level']
                    rule.rule_msg = kwargs['rule_msg']
                    rule.is_system = kwargs['is_system']
                    rule.create_by = kwargs['create_by']
                    rule.update_time = kwargs['timestamp']
                    rule.save()
                    return True, '策略更新成功'

            rule = IastVulRule(
                rule_name=kwargs['rule_name'],
                rule_level=kwargs['rule_level'],
                rule_msg=kwargs['rule_msg'],
                rule_value=kwargs['rule_value'],
                is_system=kwargs['is_system'],
                create_by=kwargs['create_by'],
                update_time=kwargs['timestamp'],
                create_time=kwargs['timestamp']
            )
            rule.save()
            return True, '策略保存成功'
        except Exception as e:
            logger.error(e)
            return False, str(e)

    def post(self, request):
        if request.user.is_active:
            rule_id, rule_name, rule_level, rule_msg, rule_value, is_system, create_by, timestamp = \
                self.parse_args(request)
            logger.info(f'保存策略，策略ID {rule_id}')
            status, msg = self.save_or_create_rule(rule_id=rule_id, rule_name=rule_name, rule_level=rule_level,
                                                   rule_msg=rule_msg, rule_value=rule_value, is_system=is_system,
                                                   create_by=create_by, timestamp=timestamp)
            if status:
                return R.success(msg=msg)
            return R.failure(msg=msg)

        else:
            return R.failure(msg='请先登录')
