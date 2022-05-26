#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from dongtai_common.utils import const
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from dongtai_web.serializers.hook_strategy import SINK_POSITION_HELP_TEXT
from rest_framework import serializers

class _HookRuleAddBodyargsSerializer(serializers.Serializer):
    rule_type_id = serializers.IntegerField(
        help_text=_('The id of hook rule type.'))
    rule_value = serializers.CharField(
        help_text=_('The value of strategy'),
        max_length=255,
    )
    rule_source = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Source of taint"),
                              SINK_POSITION_HELP_TEXT),
        max_length=255,
    )
    rule_target = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Target of taint"),
                              SINK_POSITION_HELP_TEXT),
        max_length=255,
    )
    inherit = serializers.CharField(
        help_text=
        _('Inheritance type, false-only detect current class, true-inspect subclasses, all-check current class and subclasses'
          ),
        max_length=255,
    )
    track = serializers.CharField(
        help_text=
        _("Indicates whether taint tracking is required, true-required, false-not required."
          ),
        max_length=5,
    )


_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Policy enabled success, total {} hook rules')), ''),
    ((202, _('Incomplete parameter, please check again')), ''),
    ((202, _('Failed to create strategy')), ''),
))


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

    @extend_schema_with_envcheck(
        
        request=_HookRuleAddBodyargsSerializer,
        tags=[_('Hook Rule')],
        summary=_('Hook Rule Add'),
        description=_(
            "Generate corresponding strategy group according to the strategy selected by the user."
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        rule_type, rule_value, rule_source, rule_target, inherit, is_track = self.parse_args(request)
        if all((rule_type, rule_value, rule_source, inherit, is_track)) is False:
            return R.failure(msg=_('Incomplete parameter, please check again'))

        strategy = self.create_strategy(rule_value, rule_source, rule_target, inherit, is_track, request.user.id)
        if strategy:
            hook_type = HookType.objects.filter(
                id=rule_type,
                created_by__in=(request.user.id, const.SYSTEM_USER_ID)
            ).first()
            if hook_type:
                hook_type.strategies.add(strategy)
                return R.success(msg=_('Strategy has been created successfully'))
        return R.failure(msg=_('Failed to create strategy'))
