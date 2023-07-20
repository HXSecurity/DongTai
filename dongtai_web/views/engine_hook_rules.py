#!/usr/bin/env python
import logging

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.utils import const
from dongtai_web.serializers.hook_strategy import HOOK_TYPE_CHOICE, HookRuleSerializer
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _EngineHookRulesQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        HOOK_TYPE_CHOICE,
        help_text=_(
            "type of hook rule \n 1 represents the propagation method, 2 represents the source method, 3 represents the filter method, and 4 represents the taint method"
        ),
    )
    pageSize = serializers.IntegerField(default=20, help_text=_("number per page"))
    page = serializers.IntegerField(default=1, help_text=_("page index"))
    strategy_type = serializers.IntegerField(help_text=_("The id of hook_type"), required=False)
    language_id = serializers.IntegerField(default=1, help_text=_("The id of programming language"), required=False)
    keyword = serializers.CharField(help_text=_("The keyword for search"), required=False)


_ResponseSerializer = get_response_serializer(
    data_serializer=HookRuleSerializer(many=True),
)

logger = logging.getLogger("dongtai-webapi")


class EngineHookRulesEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            ser = _EngineHookRulesQuerySerializer(data=request.GET)
            try:
                ser.is_valid(True)
            except ValidationError:
                return None, None, None, None, None, None
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
            keyword = ser.validated_data.get("keyword", None)

            strategy_type = ser.validated_data.get("strategy_type")
        except Exception as e:
            logger.exception(_("Parameter parsing failed, error message: "), exc_info=e)
            return None, None, None, None, None, None
        else:
            return rule_type, page, page_size, strategy_type, language_id, keyword

    @extend_schema_with_envcheck(
        querys=[_EngineHookRulesQuerySerializer],
        tags=[_("Hook Rule")],
        summary=_("Hook Rule List"),
        description=_("Get the list of hook strategies"),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        res = self.parse_args(request)
        if res is None:
            return R.failure(msg=_("Parameter error"))
        rule_type, page, page_size, strategy_type, language_id, keyword = res
        if all(x is not None for x in [rule_type, page, page_size, language_id]) is False:
            return R.failure(msg=_("Parameter error"))
        if rule_type is None:
            return R.failure(msg=_("Strategy type does not exist"))

        try:
            if rule_type == 4:
                if strategy_type:
                    rule_type_queryset = IastStrategyModel.objects.filter(
                        pk=strategy_type,
                    )
                else:
                    rule_type_queryset = IastStrategyModel.objects.all()
            elif strategy_type:
                rule_type_queryset = HookType.objects.filter(id=strategy_type, type=rule_type, language_id=language_id)
            else:
                rule_type_queryset = HookType.objects.filter(type=rule_type, language_id=language_id)
            if rule_type == 4:
                q = (
                    Q(strategy__in=rule_type_queryset)
                    & Q(enable__in=(const.ENABLE, const.DISABLE))
                    & Q(language_id=language_id)
                )
            else:
                q = Q(hooktype__in=rule_type_queryset) & Q(enable__in=(const.ENABLE, const.DISABLE))
            if keyword:
                q = Q(value__icontains=keyword) & q
            rule_queryset = HookStrategy.objects.filter(q)
            page_summary, queryset = self.get_paginator(rule_queryset.order_by("-id"), page=page, page_size=page_size)
            if rule_type == 4:
                queryset = queryset.select_related("strategy")
            else:
                queryset = queryset.select_related("hooktype")
            data = HookRuleSerializer(queryset, many=True).data
            return R.success(data=data, page=page_summary)
        except Exception as e:
            logger.exception(_("Rule read error, error message: {}"), exc_info=e)
            return R.failure()
