#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午3:00
# software: PyCharm
# project: lingzhi-webapi
from dongtai.utils import const
from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from iast.serializers.strategy import StrategySerializer


class StrategyEndpoint(UserEndPoint):
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
                    1  # 删除该字段
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
            return R.success(msg='暂无策略')
