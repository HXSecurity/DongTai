#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/9 下午12:06
# software: PyCharm
# project: lingzhi-engine
import time

from lingzhi_engine.base import R
from vuln.base.method_pool import UserEndPoint
from vuln.models.hook_strategy import HookStrategy


class HookRuleModifyEndPoint(UserEndPoint):
    def parse_args(self, request):
        """
        :param request:
        :return:
        """
        try:
            rule_id = request.data.get('rule_id').strip()
            rule_type = request.data.get('rule_type_id').strip()
            rule_value = request.data.get('rule_value').strip()
            rule_source = request.data.get('rule_source').strip()
            rule_target = request.data.get('rule_target').strip()
            inherit = request.data.get('inherit').strip()
            is_track = request.data.get('track').strip()

            return rule_id, rule_type, rule_value, rule_source, rule_target, inherit, is_track
        except Exception as e:
            # todo 增加异场打印
            return None, None, None, None, None, None, None

    def get(self, request):
        rule_id, rule_type, rule_value, rule_source, rule_target, inherit, is_track = self.parse_args(request)
        if all((rule_id, rule_type, rule_value, rule_source, rule_target, inherit, is_track)) is False:
            return R.failure(msg='策略类型不存在')

        strategy = HookStrategy.objects.filter(id=rule_id, created_by=request.user.id).first()

        if strategy:
            strategy.value = rule_value
            strategy.source = rule_source
            strategy.target = rule_target
            strategy.inherit = inherit
            strategy.track = is_track
            strategy.update_time = int(time.time())
            strategy.save()

            return R.success(msg='策略创建成功')
        return R.failure(msg='策略创建失败')
