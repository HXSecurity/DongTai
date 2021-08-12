#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from dongtai.utils import const
from django.utils.translation import gettext_lazy as _


class EngineHookRuleAddEndPoint(UserEndPoint):
    def parse_args(self, request):
        """
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
            
            return None, None, None, None, None, None

    def create_strategy(self, value, source, target, inherit, track, created_by):
        try:
            
            
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
            return R.failure(msg=_('The parameter is incomplete, please check'))

        strategy = self.create_strategy(rule_value, rule_source, rule_target, inherit, is_track, request.user.id)
        if strategy:
            hook_type = HookType.objects.filter(
                id=rule_type,
                created_by__in=(request.user.id, const.SYSTEM_USER_ID)
            ).first()
            if hook_type:
                hook_type.strategies.add(strategy)
                return R.success(msg=_('Strategy creation success'))
        return R.failure(msg=_('Strategy creation failed'))
