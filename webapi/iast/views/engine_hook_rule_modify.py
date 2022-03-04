#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time

from dongtai.endpoint import UserEndPoint, R
from dongtai.utils import const
from dongtai.models.hook_strategy import HookStrategy
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from django.utils.text import format_lazy
from iast.serializers.hook_strategy import SINK_POSITION_HELP_TEXT
from dongtai.models.hook_type import HookType


_PostResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('strategy has been created successfully')), ''),
    ((202, _('Incomplete parameter, please check again')), ''),
    ((202, _('Failed to create strategy')), ''),
))


class _EngineHookRuleModifySerializer(serializers.Serializer):
    rule_id = serializers.IntegerField(
        help_text=_('The id of hook rule'))
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


class EngineHookRuleModifyEndPoint(UserEndPoint):
    def parse_args(self, request):
        """
        :param request:
        :return:
        """
        try:
            rule_id = request.data.get('rule_id')
            rule_type = request.data.get('rule_type_id')
            rule_value = request.data.get('rule_value').strip()
            rule_source = request.data.get('rule_source').strip()
            rule_target = request.data.get('rule_target').strip()
            inherit = request.data.get('inherit').strip()
            is_track = request.data.get('track').strip()

            return rule_id, rule_type, rule_value, rule_source, rule_target, inherit, is_track
        except Exception as e:
            return None, None, None, None, None, None, None

    @extend_schema_with_envcheck(
        request=_EngineHookRuleModifySerializer,
        tags=[_('Hook Rule')],
        summary=_('Hook Rule Modify'),
        description=_("Modify the rule corresponding to the specified id"),
        response_schema=_PostResponseSerializer,
    )
    def post(self, request):
        rule_id, rule_type, rule_value, rule_source, rule_target, inherit, is_track = self.parse_args(request)
        hook_type = HookType.objects.filter(
                id=rule_type,
                created_by__in=(request.user.id, const.SYSTEM_USER_ID)
            ).first()
        if all((rule_id, rule_type, rule_value, rule_source, inherit, is_track, hook_type)) is False:
            return R.failure(msg=_('Incomplete parameter, please check again'))

        strategy = HookStrategy.objects.filter(id=rule_id, created_by=request.user.id).first()
        if strategy:
            if hook_type:
                strategy.type.get(strategy=strategy).strategies.remove(strategy)
                hook_type.strategies.add(strategy)
            strategy.value = rule_value
            strategy.source = rule_source
            strategy.target = rule_target
            strategy.inherit = inherit
            strategy.track = is_track
            strategy.update_time = int(time.time())
            strategy.save()

            return R.success(msg=_('strategy has been created successfully'))
        return R.failure(msg=_('Failed to create strategy'))
