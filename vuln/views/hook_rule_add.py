#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/9 下午12:06
# software: PyCharm
# project: lingzhi-engine
import time

from lingzhi_engine import const
from lingzhi_engine.base import R
from vuln.base.method_pool import UserEndPoint
from vuln.models.hook_strategy import HookStrategy
from vuln.models.hook_type import HookType


class HookRuleAddEndPoint(UserEndPoint):
    def parse_args(self, request):
        """
        规则类型ID
        规则详情
        污点来源
        污点去向
        是否跟踪
        继承深度
        :param request:
        :return:
        """
        try:
            rule_type = request.data.get('rule_type_id')
            rule_value = request.data.get('rule_value').strip()
            rule_source = request.data.get('rule_source').strip()
            rule_target = request.data.get('rule_target').strip()
            inherit = request.data.get('inherit').strip()
            is_track = request.data.get('track').strip()

            return rule_type, rule_value, rule_source, rule_target, inherit, is_track
        except Exception as e:
            # todo 增加异场打印
            return None, None, None, None, None, None

    def create_strategy(self, value, source, target, inherit, track, created_by):
        try:
            # todo 考虑将前端发送的数据进行转换
            # 前端直接处理为最终的数据格式？
            timestamp = int(time.time())
            strategy = HookStrategy(
                value=value,
                source=source,
                target=target,
                inherit=inherit,
                track=track,
                create_time=timestamp,
                update_time=timestamp,
                created_by=created_by,
                enable=const.ENABLE
            )
            strategy.save()
            return strategy
        except Exception as e:
            return None

    def post(self, request):
        rule_type, rule_value, rule_source, rule_target, inherit, is_track = self.parse_args(request)
        if all((rule_type, rule_value, rule_source, inherit, is_track)) is False:
            return R.failure(msg='参数不完整，请检查')

        strategy = self.create_strategy(rule_value, rule_source, rule_target, inherit, is_track, request.user.id)
        if strategy:
            hook_type = HookType.objects.filter(id=rule_type,
                                                created_by__in=(request.user.id, const.SYSTEM_USER_ID)).first()
            if hook_type:
                hook_type.strategies.add(strategy)
                return R.success(msg='策略创建成功')
        return R.failure(msg='策略创建失败')
