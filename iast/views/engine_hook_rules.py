#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from dongtai.utils import const

from iast.serializers.hook_strategy import HookRuleSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer

from rest_framework import serializers

class _EngineHookRulesQuerySerializer(serializers.Serializer):
    type = serializers.IntegerField(help_text=_(
        "type of hook rule \n 1 represents the propagation method, 2 represents the source method, 3 represents the filter method, and 4 represents the taint method"
    ))
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('number per page'))
    page = serializers.IntegerField(default=1, help_text=_('page index'))
    strategy_type = serializers.IntegerField(
        help_text=_("The id of hook_type"), required=False)


_ResponseSerializer = get_response_serializer(
    data_serializer=HookRuleSerializer(many=True), )

logger = logging.getLogger('dongtai-webapi')


class EngineHookRulesEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_type = request.query_params.get('type', const.RULE_PROPAGATOR)
            rule_type = int(rule_type)
            if rule_type not in (
                    const.RULE_SOURCE, const.RULE_ENTRY_POINT, const.RULE_PROPAGATOR, const.RULE_FILTER,
                    const.RULE_SINK):
                rule_type = None

            page = request.query_params.get('page', 1)
            page = int(page)

            page_size = request.query_params.get('pageSize', 20)
            page_size = int(page_size)
            if page_size > const.MAX_PAGE_SIZE:
                page_size = const.MAX_PAGE_SIZE


            strategy_type = request.query_params.get('strategy_type')
            return rule_type, page, page_size, strategy_type
        except Exception as e:
            logger.error(_("Parameter parsing failed, error message: {}").format(e))
            return None, None, None

    @extend_schema_with_envcheck(
        querys=[_EngineHookRulesQuerySerializer],
        tags=[_('Hook Rule')],
        summary=_('Hook Rule List'),
        description=_("Get the list of hook strategies"),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        rule_type, page, page_size, strategy_type = self.parse_args(request)
        if rule_type is None:
            return R.failure(msg=_('Strategy type does not exist'))

        try:
            user_id = request.user.id
            if strategy_type:
                rule_type_queryset = HookType.objects.filter(id=strategy_type,
                                                             created_by__in=(user_id, const.SYSTEM_USER_ID),
                                                             type=rule_type)
            else:
                rule_type_queryset = HookType.objects.filter(created_by__in=(user_id, const.SYSTEM_USER_ID),
                                                             type=rule_type)
            rule_queryset = HookStrategy.objects.filter(type__in=rule_type_queryset, created_by=user_id)
            page_summary, queryset = self.get_paginator(rule_queryset, page=page, page_size=page_size)
            data = HookRuleSerializer(queryset, many=True).data
            return R.success(data=data, page=page_summary)
        except Exception as e:
            logger.error(_("Rule read error, error message: {}").format(e))
            return R.failure()
