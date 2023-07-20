#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vul_level import IastVulLevel
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

from rest_framework import serializers


class _StrategyTypeResponseDataTypeValueSerializer(serializers.Serializer):
    strategy_id = serializers.CharField(help_text=_("The id of strategy"))
    vul_name = serializers.CharField(
        help_text=_("The name of the vulnerability type targeted by the strategy")
    )
    level_id = serializers.IntegerField(
        help_text=_("The strategy corresponds to the level of vulnerability")
    )


class _StrategyTypeResponseDataStrategySerializer(serializers.Serializer):
    level_id = serializers.IntegerField(help_text=_("Level id of vulnerability"))
    level_name = serializers.IntegerField(help_text=_("Level name of vulnerability"))
    type_value = _StrategyTypeResponseDataTypeValueSerializer(many=True)


_ResponseSerializer = get_response_serializer(
    data_serializer=_StrategyTypeResponseDataStrategySerializer(many=True),
)


class StrategyType(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Strategy")],
        summary=_("Strategy Type"),
        description=_("Get a list of strategy types."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        queryset = IastStrategyModel.objects.filter(state="enable").select_related(
            "level"
        )
        allType = IastVulLevel.objects.all().order_by("id")
        result = []
        curTyp = {}
        if queryset:
            for item in queryset:
                if not item.level:
                    continue
                if item.level.id not in curTyp.keys():
                    curTyp[item.level_id] = []
                curTyp[item.level_id].append(
                    {
                        "strategy_id": item.id,
                        "level_id": item.level_id,
                        "vul_name": item.vul_name,
                    }
                )
        if allType:
            for item in allType:
                result.append(
                    {
                        "level_id": item.id,
                        "level_name": item.name_type,
                        "type_value": curTyp.get(item.id, []),
                    }
                )
        return R.success(data=result)
