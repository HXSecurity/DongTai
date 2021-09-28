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


class EngineHookRuleSummarySerializer(serializers.Serializer):
    typeCount = serializers.IntegerField(
        help_text=_("Total number of rule types"))
    ruleCount = serializers.IntegerField(help_text=_("Total number of rules"))
    sinkCount = serializers.IntegerField(
        help_text=_("Total number of sink type rules"))


_ResponseSerializer = get_response_serializer(
    EngineHookRuleSummarySerializer(many=True))


class EngineHookRuleSummaryEndPoint(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_('Hook Rule')],
        summary=_('Hook Rule Summary'),
        description=_("Statistics on the number of hook rules"),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        rule_type_queryset = HookType.objects.filter(created_by__in=[request.user.id, const.SYSTEM_USER_ID])
        rule_type_count = rule_type_queryset.values('id').count()

        sink_type_queryset = rule_type_queryset.filter(type=const.RULE_SINK)
        sink_count = HookStrategy.objects.values('id').filter(type__in=sink_type_queryset).count()

        rule_count = HookStrategy.objects.values('id').filter(type__in=rule_type_queryset).count()
        return R.success(data={
            'typeCount': rule_type_count,
            'ruleCount': rule_count,
            'sinkCount': sink_count
        })
