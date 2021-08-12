#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_type import HookType
from dongtai.utils import const
from django.utils.translation import gettext_lazy as _


class EngineHookRuleTypeAddEndPoint(UserEndPoint):
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
            
            return None, None, None, None

    def post(self, request):
        rule_type, name, short_name, enable = self.parse_args(request)
        if all((rule_type, name, short_name)) is False:
            return R.failure(msg=_('incomplete data'))
        timestamp = int(time.time())
        hook_type = HookType(enable=enable, type=rule_type, name=short_name, value=name, create_time=timestamp,
                             update_time=timestamp, created_by=request.user.id)
        hook_type.save()
        return R.success(msg=_('Rule type Save success'))
