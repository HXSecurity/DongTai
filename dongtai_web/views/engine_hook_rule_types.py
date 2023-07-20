#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.hook_type import HookType
from dongtai_common.utils import const

from dongtai_web.serializers.hook_type_strategy import (
    HookTypeSerialize,
    StrategySerialize,
)
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from rest_framework.serializers import ValidationError
from dongtai_web.serializers.hook_strategy import HOOK_TYPE_CHOICE
from dongtai_common.models.strategy import IastStrategyModel

logger = logging.getLogger("dongtai-webapi")


class _EngineHookRuleTypeArgsSerializer(serializers.Serializer):
    pageSize = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    type = serializers.ChoiceField(
        HOOK_TYPE_CHOICE,
        help_text=_(
            "type of hook rule \n 1 represents the propagation method, 2 represents the source method, 3 represents the filter method, and 4 represents the taint method"
        ),
    )
    language_id = serializers.IntegerField(
        default=1, help_text=_("The id of programming language"), required=False
    )


_SuccessSerializer = get_response_serializer(
    HookTypeSerialize(many=True, allow_null=True)
)


class EngineHookRuleTypesEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            ser = _EngineHookRuleTypeArgsSerializer(data=request.GET)
            try:
                ser.is_valid(True)
            except ValidationError as e:
                return None, None, None, None
            rule_type = ser.validated_data.get("type", const.RULE_PROPAGATOR)
            rule_type = int(rule_type)
            if rule_type not in (
                const.RULE_SOURCE,
                const.RULE_ENTRY_POINT,
                const.RULE_PROPAGATOR,
                const.RULE_FILTER,
                const.RULE_SINK,
            ):
                rule_type = None

            page = ser.validated_data.get("page", 1)
            page = int(page)

            page_size = ser.validated_data.get("pageSize", 20)
            page_size = int(page_size)
            if page_size > const.MAX_PAGE_SIZE:
                page_size = const.MAX_PAGE_SIZE
            language_id = ser.validated_data.get("language_id", 1)
            return rule_type, page, page_size, language_id
        except Exception as e:
            logger.error(_("Parameter parsing failed, error message: {}").format(e))
            return None, None, None, None

    @extend_schema_with_envcheck(
        [_EngineHookRuleTypeArgsSerializer],
        response_schema=_SuccessSerializer,
        summary=_("Hook Types List"),
        description=_("Get Hook Types List"),
        tags=[_("Hook Rule")],
    )
    def get(self, request):
        rule_type, page, page_size, language_id = self.parse_args(request)
        if (
            all(map(lambda x: x is not None, [rule_type, page, page_size, language_id]))
            is False
        ):
            return R.failure(msg=_("Parameter error"))
        if rule_type is None:
            return R.failure(msg=_("Strategy type does not exist"))
        if rule_type == 4:
            queryset = IastStrategyModel.objects.filter(
                state__in=["enable", "disable"]
            ).all()
            data = StrategySerialize(queryset, many=True).data
        else:
            queryset = HookType.objects.filter(
                created_by__in=[request.user.id, const.SYSTEM_USER_ID],
                type=rule_type,
                language_id=language_id,
            )
            data = HookTypeSerialize(queryset, many=True).data
        return R.success(data=data)
