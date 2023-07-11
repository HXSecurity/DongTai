#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.utils import const
from dongtai_common.models.hook_strategy import HookStrategy
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.utils.text import format_lazy
from dongtai_web.serializers.hook_strategy import SINK_POSITION_HELP_TEXT
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.common.agent_command_check import (
    tag_validator,
    taint_command_validator,
)

_PostResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('strategy has been created successfully')), ''),
    ((202, _('Incomplete parameter, please check again')), ''),
    ((202, _('Failed to create strategy')), ''),
))


class _EngineHookRuleModifySerializer(serializers.Serializer):
    rule_id = serializers.IntegerField(help_text=_('The id of hook rule'))
    rule_type_id = serializers.IntegerField(
        help_text=_('The id of hook rule type.'))
    rule_value = serializers.CharField(
        help_text=_('The value of strategy'),
        max_length=255,
        allow_blank=True,
    )
    rule_source = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Source of taint"),
                              SINK_POSITION_HELP_TEXT),
        max_length=255,
        allow_blank=True,
    )
    rule_target = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Target of taint"),
                              SINK_POSITION_HELP_TEXT),
        max_length=255,
        allow_blank=True,
    )
    inherit = serializers.CharField(
        help_text=_('Inheritance type, false-only detect current class, true-inspect subclasses, all-check current class and subclasses'),
        max_length=255,
    )
    track = serializers.CharField(
        help_text=_("Indicates whether taint tracking is required, true-required, false-not required."),
        max_length=5,
    )
    ignore_blacklist = serializers.BooleanField(
        help_text=_("ignore_blacklist "),
        required=False,
        default=False,
    )
    ignore_internal = serializers.BooleanField(
        help_text=_("ignore_internal "),
        required=False,
        default=False,
    )
    tags = serializers.ListField(
        child=serializers.CharField(validators=[tag_validator]),
        required=False,
        default=list,
    )
    untags = serializers.ListField(
        child=serializers.CharField(validators=[tag_validator]),
        required=False,
        default=list,
    )
    command = serializers.CharField(
        max_length=256,
        validators=[taint_command_validator],
        required=False,
        default="",
        allow_blank=True,
    )
    stack_blacklist = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
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
            ignore_blacklist = request.data.get('ignore_blacklist', False)
            ignore_internal = request.data.get('ignore_internal', False)

            return (rule_id, rule_type, rule_value, rule_source, rule_target,
                    inherit, is_track, ignore_blacklist, ignore_internal)

        except Exception as e:
            return None, None, None, None, None, None, None, None, None

    @extend_schema_with_envcheck(
        request=_EngineHookRuleModifySerializer,
        tags=[_('Hook Rule')],
        summary=_('Hook Rule Modify'),
        description=_("Modify the rule corresponding to the specified id"),
        response_schema=_PostResponseSerializer,
    )
    def post(self, request):
        # bad parameter parse and validate example, don't do this again.
        # don't use it again when old fields change.
        (rule_id, rule_type, rule_value, rule_source, rule_target, inherit,
         is_track, ignore_blacklist,
         ignore_internal) = self.parse_args(request)
        strategy = HookStrategy.objects.filter(id=rule_id).first()
        if not strategy:
            return R.failure(msg=_('No such hookstrategy.'))
        if strategy.type == 4:
            hook_type = IastStrategyModel.objects.filter(
                id=rule_type, ).first()
        else:
            hook_type = HookType.objects.filter(id=rule_type, ).first()
        if all((rule_id, rule_type, rule_value, rule_source, inherit, is_track,
                strategy)) is False:
            return R.failure(msg=_('Incomplete parameter, please check again'))

        ser = _EngineHookRuleModifySerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail,
                             msg=_('Incomplete parameter, please check again'))

        if strategy:
            if hook_type and strategy.type == 4:
                strategy.strategy = hook_type
            else:
                strategy.hooktype = hook_type
            strategy.value = rule_value
            strategy.source = rule_source
            strategy.target = rule_target
            strategy.inherit = inherit
            strategy.track = is_track
            strategy.update_time = int(time.time())
            strategy.ignore_blacklist = ignore_blacklist
            strategy.ignore_internal = ignore_internal
            strategy.tags = ser.validated_data['tags']
            strategy.untags = ser.validated_data['untags']
            strategy.command = ser.validated_data['command']
            strategy.stack_blacklist = ser.validated_data['stack_blacklist']
            strategy.save()

            return R.success(msg=_('strategy has been created successfully'))
        return R.failure(msg=_('Failed to create strategy'))
