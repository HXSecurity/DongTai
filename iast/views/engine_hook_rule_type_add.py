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
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from iast.serializers.hook_strategy import HOOK_TYPE_CHOICE

ENABLE_CHOICE = (const.ENABLE, const.DISABLE)


class _EngineHookRuleTypeAddSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        HOOK_TYPE_CHOICE,
        help_text=
        _("type of hook rule \n 1 represents the propagation method, 2 represents the source method, 3 represents the filter method, and 4 represents the taint method"
          ))
    enable = serializers.ChoiceField(
        ENABLE_CHOICE,
        help_text=_(
            "The enabled state of the hook strategy: 0-disabled, 1-enabled"))
    name = serializers.CharField(help_text=_("The name of hook type"),
                                 max_length=255)
    short_name = serializers.CharField(
        help_text=_("The short name of hook type"), max_length=255)


_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Rule type successfully saved')), ''),
    ((202, _('Incomplete data')), ''),
))


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

    @extend_schema_with_envcheck(
        request=_EngineHookRuleTypeAddSerializer,
        tags=[_('Hook Rule')],
        summary=_('Hook Rule Type Add'),
        description=_("Create hook rule type based on incoming parameters"),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        rule_type, name, short_name, enable = self.parse_args(request)
        if all((rule_type, name, short_name)) is False:
            return R.failure(msg=_('Incomplete data'))
        timestamp = int(time.time())
        hook_type = HookType(enable=enable, type=rule_type, name=short_name, value=name, create_time=timestamp,
                             update_time=timestamp, created_by=request.user.id)
        hook_type.save()
        return R.success(msg=_('Rule type successfully saved'))
