#!/usr/bin/env python
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from dongtai_common.utils import const
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class EngineHookRuleSummarySerializer(serializers.Serializer):
    typeCount = serializers.IntegerField(help_text=_("Total number of rule types"))
    ruleCount = serializers.IntegerField(help_text=_("Total number of rules"))
    sinkCount = serializers.IntegerField(help_text=_("Total number of sink type rules"))


class _EngineHookRuleSummaryQuerySerializer(serializers.Serializer):
    language_id = serializers.IntegerField(
        help_text=_("The id of programming language"), required=False, allow_null=True
    )


_ResponseSerializer = get_response_serializer(EngineHookRuleSummarySerializer(many=True))


class EngineHookRuleSummaryEndPoint(UserEndPoint):
    @extend_schema_with_envcheck(
        [_EngineHookRuleSummaryQuerySerializer],
        tags=[_("Hook Rule")],
        summary=_("Hook Rule Summary"),
        description=_("Statistics on the number of hook rules"),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        ser = _EngineHookRuleSummaryQuerySerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError:
            return R.failure(msg=_("Parameter error"))
        rule_type_queryset = HookType.objects.filter(created_by__in=[request.user.id, const.SYSTEM_USER_ID])
        if ser.validated_data.get("language_id", None):
            rule_type_queryset = rule_type_queryset.filter(language_id=ser.validated_data["language_id"], enable__gt=0)
        rule_type_count = rule_type_queryset.values("id").count()

        rule_type_queryset.filter(type=const.RULE_SINK)
        sink_queryset = HookStrategy.objects.values("id").filter(type__in=[4], enable__gt=0)
        rule_queryset = HookStrategy.objects.values("id").filter(type__in=[1, 2, 3], enable__gt=0)
        if ser.validated_data.get("language_id", None):
            sink_queryset = sink_queryset.filter(language_id=ser.validated_data["language_id"])
            rule_queryset = rule_queryset.filter(language_id=ser.validated_data["language_id"])
        sink_count = sink_queryset.count()

        rule_count = rule_queryset.count()
        return R.success(
            data={
                "typeCount": rule_type_count,
                "ruleCount": rule_count,
                "sinkCount": sink_count,
            }
        )
