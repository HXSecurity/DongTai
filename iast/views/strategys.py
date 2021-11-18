#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi
from dongtai.utils import const
from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from iast.serializers.strategy import StrategySerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer

from rest_framework import serializers
class _StrategyResponseDataStrategySerializer(serializers.Serializer):
    id = serializers.CharField(help_text=_('The id of agent'))
    vul_name = serializers.CharField(help_text=_('The name of the vulnerability type targeted by the strategy'))
    vul_type = serializers.CharField(help_text=_('Types of vulnerabilities targeted by the strategy'))
    enable = serializers.CharField(help_text=_('This field indicates whether the vulnerability is enabled, 1 or 0'))
    vul_desc = serializers.CharField(help_text=_('Description of the corresponding vulnerabilities of the strategy'))
    level = serializers.IntegerField(
        help_text=_('The strategy corresponds to the level of vulnerability'))
    dt = serializers.IntegerField(
        help_text=_('Strategy update time'))
    vul_fix = serializers.CharField(help_text=_(
        "Suggestions for repairing vulnerabilities corresponding to the strategy"
    ))




_ResponseSerializer = get_response_serializer(
    data_serializer=_StrategyResponseDataStrategySerializer(many=True), )


class StrategyEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_('Strategy')],
        summary=_('Strategy List'),
        description=_(
            "Get a list of strategies."
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        strategy_models = HookType.objects.values(
            'id', 'name', 'value',
            'enable').filter(type=const.RULE_SINK).exclude(enable=const.DELETE)
        if strategy_models:
            models = dict()
            for strategy_model in strategy_models:
                models[strategy_model['id']] = {
                    'id':
                    strategy_model['id'],
                    'vul_name':
                    strategy_model['name'],
                    'vul_type':
                    strategy_model['value'],
                    'state':
                    const.STRATEGY_DISABLE
                    if strategy_model['enable'] is not None
                    and strategy_model['enable'] == 0 else
                    const.STRATEGY_ENABLE,
                    'vul_desc':
                    '',
                    'level':
                    1,
                    'dt':
                    1
                }

            strategy_ids = models.keys()
            profiles = IastStrategyModel.objects.values(
                'level_id', 'vul_desc', 'vul_fix',
                'hook_type_id').filter(hook_type_id__in=strategy_ids)
            if profiles:
                for profile in profiles:
                    strategy_id = profile.get('hook_type_id')
                    models[strategy_id]['vul_desc'] = profile['vul_desc']
                    models[strategy_id]['vul_fix'] = profile['vul_fix']
                    models[strategy_id]['level'] = profile['level_id']
            return R.success(data=list(models.values()))
        else:
            return R.success(msg=_('No strategy'))
