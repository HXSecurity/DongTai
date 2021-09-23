#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_type import HookType
from dongtai.utils import const

from iast.serializers.hook_type_strategy import HookTypeSerialize
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
logger = logging.getLogger('dongtai-webapi')
HOOK_TYPE_CHOICE = (const.RULE_SOURCE, const.RULE_ENTRY_POINT,
                    const.RULE_PROPAGATOR, const.RULE_FILTER, const.RULE_SINK)


class _EngineHookRuleTypeArgsSerializer(serializers.Serializer):
    pageSize = serializers.IntegerField(default=20,
                                        help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    type = serializers.ChoiceField(
        HOOK_TYPE_CHOICE,
        help_text=
        _("type of hook rule \n 1 represents the propagation method, 2 represents the source method, 3 represents the filter method, and 4 represents the taint method"
          ))

_SuccessSerializer = get_response_serializer(
    HookTypeSerialize(many=True, allow_null=True))


class EngineHookRuleTypesEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_type = request.query_params.get('type', const.RULE_PROPAGATOR)
            rule_type = int(rule_type)
            if rule_type not in (const.RULE_SOURCE, const.RULE_ENTRY_POINT,
                                 const.RULE_PROPAGATOR, const.RULE_FILTER,
                                 const.RULE_SINK):
                rule_type = None

            page = request.query_params.get('page', 1)
            page = int(page)

            page_size = request.query_params.get('pageSize', 20)
            page_size = int(page_size)
            if page_size > const.MAX_PAGE_SIZE:
                page_size = const.MAX_PAGE_SIZE

            return rule_type, page, page_size
        except Exception as e:
            logger.error(_("Parameter parsing failed, error message: {}").format(e))
            return None, None, None

    @extend_schema_with_envcheck([_EngineHookRuleTypeArgsSerializer],
                                 response_schema=_SuccessSerializer,
                                 summary=_('Hook Types List'),
                                 description=_("Get Hook Types List"),
                                 tags=[_('Hook Rule')])
    def get(self, request):
        rule_type, page, page_size = self.parse_args(request)
        if rule_type is None:
            return R.failure(msg=_('Strategy type does not exist'))

        queryset = HookType.objects.filter(created_by__in=[request.user.id, const.SYSTEM_USER_ID], type=rule_type)
        data = HookTypeSerialize(queryset, many=True).data
        return R.success(data=data)
