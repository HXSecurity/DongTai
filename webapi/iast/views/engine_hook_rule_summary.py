#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from dongtai.utils import const
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


class EngineHookRuleSummarySerializer(serializers.Serializer):
    typeCount = serializers.IntegerField(
        help_text=_("Total number of rule types"))
    ruleCount = serializers.IntegerField(help_text=_("Total number of rules"))
    sinkCount = serializers.IntegerField(
        help_text=_("Total number of sink type rules"))


class _EngineHookRuleSummaryQuerySerializer(serializers.Serializer):
    language_id = serializers.IntegerField(
        help_text=_('The id of programming language'),
        required=False,allow_null=True)


_ResponseSerializer = get_response_serializer(
    EngineHookRuleSummarySerializer(many=True))


class EngineHookRuleSummaryEndPoint(UserEndPoint):
    @extend_schema_with_envcheck(
        [_EngineHookRuleSummaryQuerySerializer],
        tags=[_('Hook Rule')],
        summary=_('Hook Rule Summary'),
        description=_("Statistics on the number of hook rules"),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        ser = _EngineHookRuleSummaryQuerySerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError as e:
            return R.failure(msg=_('Parameter error'))
        rule_type_queryset = HookType.objects.filter(created_by__in=[request.user.id, const.SYSTEM_USER_ID])
        if ser.validated_data.get('language_id', None):
            rule_type_queryset = rule_type_queryset.filter(
                language_id=ser.validated_data['language_id'], enable__gt=0)
        rule_type_count = rule_type_queryset.values('id').count()

        sink_type_queryset = rule_type_queryset.filter(type=const.RULE_SINK)
        sink_count = HookStrategy.objects.values('id').filter(type__in=sink_type_queryset,enable__gt=0).count()

        rule_count = HookStrategy.objects.values('id').filter(type__in=rule_type_queryset,enable__gt=0).count()
        return R.success(data={
            'typeCount': rule_type_count,
            'ruleCount': rule_count,
            'sinkCount': sink_count
        })
