#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_strategy import HookStrategy
from dongtai.utils import const
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('dongtai-webapi')


class EngineHookRuleTypeEnableEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_id = request.query_params.get('rule_id', const.RULE_PROPAGATOR)
            rule_type = int(rule_id)
            return rule_type
        except Exception as e:
            logger.error(_("Parameter processing failed, error details: {}").format(e))
            return None

    def get(self, request):
        rule_id = self.parse_args(request)
        if rule_id is None:
            return R.failure(msg=_('No strategy does not exist'))

        rule = HookStrategy.objects.filter(id=rule_id, created_by=request.user.id).first()
        if rule:
            rule_type = rule.type.first()
            if rule_type:
                rule_type.enable = const.ENABLE
                rule.save()
                return R.success(msg=_('Enable success'))
        return R.failure(msg=_('Strategy type does not exist'))
