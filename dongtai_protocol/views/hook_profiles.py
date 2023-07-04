#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:16
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from drf_spectacular.utils import extend_schema
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.utils import const
from dongtai_common.endpoint import OpenApiEndPoint, R
from django.db.models import (Prefetch, OuterRef, Subquery)
# note: 当前依赖必须保留，否则无法通过hooktype反向查找策略
from dongtai_protocol.api_schema import DongTaiParameter
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

logger = logging.getLogger("django")
JAVA = 1
LANGUAGE_DICT = {'JAVA': 1, 'PYTHON': 2, 'PHP': 3, 'GO': 4}

STATE_DICT = {"enable": 1, "disable": 0, "delete": -1}


def convert_strategy(strategy: IastStrategyModel):
    strategy.value = strategy.vul_type
    strategy.name = strategy.vul_name
    strategy.enable = STATE_DICT[strategy.state]
    strategy.type = 4
    return strategy


class HookProfilesEndPoint(OpenApiEndPoint):
    name = "api-v1-profiles"
    description = "获取HOOK策略"

    @staticmethod
    def get_profiles(user=None, language_id=JAVA, full=False, system_only=False):
        profiles = list()
        hook_types = IastStrategyModel.objects.filter(
            Q(state__in=['enable'] if not full else ['enable', 'disable'],
              user_id__in=set([1, user.id]) if user else [1])
            & (Q(system_type=1) if system_only else Q())).order_by('id')
        hook_types_a = HookType.objects.filter(
            Q(language_id=language_id,
              enable__in=[const.HOOK_TYPE_ENABLE] if not full else
              [const.HOOK_TYPE_ENABLE, const.HOOK_TYPE_DISABLE],
              created_by__in=set([1, user.id]) if user else [1],
              type__in=(1, 2, 3))
            & (Q(system_type=1) if system_only else Q())).order_by('id')
        for hook_type in list(hook_types) + list(hook_types_a):
            strategy_details = list()
            if isinstance(hook_type, IastStrategyModel):
                hook_type = convert_strategy(hook_type)
            strategies = hook_type.strategies.filter(
                Q(language_id=language_id,
                  type__in=(1, 2, 3)
                  if not isinstance(hook_type, IastStrategyModel) else [4],
                  created_by__in=[1, user.id] if user else [1],
                  enable=const.HOOK_TYPE_ENABLE)
                & (Q(system_type=1) if system_only else Q())).order_by('id')
            if full:
                from django.forms.models import model_to_dict
                if not strategies.count():
                    continue
                profile = {
                    'type':
                    hook_type.type,
                    'enable':
                    hook_type.enable,
                    'value':
                    hook_type.value,
                    "details":
                    sorted([
                        model_to_dict(i,
                                      exclude=[
                                          "id", "hooktype", "create_time",
                                          "strategy", "update_time"
                                      ]) for i in strategies
                    ],
                        key=lambda item: item['value'])
                }
                profiles.append(profile)
            else:
                for strategy in strategies.values():
                    strategy_details.append({
                        "source": strategy.get("source"),
                        "track": strategy.get("track"),
                        "target": strategy.get("target"),
                        "value": strategy.get("value"),
                        "inherit": strategy.get("inherit"),
                        "ignore_blacklist": strategy.get("ignore_blacklist"),
                        "ignore_internal": strategy.get("ignore_internal"),
                        "tags": strategy.get("tags"),
                        "untags": strategy.get("untags"),
                        "command": strategy.get("command"),
                        "stack_blacklist": strategy.get("stack_blacklist"),
                    })
                strategy_details = sorted(strategy_details,
                                          key=lambda item: str(item['value']))
                if not strategy_details:
                    continue
                profiles.append({
                    'type': hook_type.type,
                    'enable': hook_type.enable,
                    'value': hook_type.value,
                    'details': strategy_details
                })
        profiles = sorted(profiles,
                          key=lambda item: (item['value'], item['type']))
        return profiles

    @extend_schema(
        description='Pull Agent Engine Hook Rule',
        parameters=[
            DongTaiParameter.LANGUAGE,
        ],
        responses=R,
        methods=['GET'],
        summary="Pull Agent Engine Hook Rule",
        tags=['Agent服务端交互协议'],
    )
    def get(self, request):
        user = request.user

        language = request.query_params.get('language')
        language_id = LANGUAGE_DICT.get(language,
                                        None) if language is not None else None
        language_id = JAVA if language_id is None and language is None else language_id
        profiles = self.get_profiles(user, language_id)

        return R.success(data=profiles)


#    def put(self, request):
#        pass
#
#    def post(self):
#        pass

if __name__ == '__main__':
    strategy_count = HookStrategy.objects.count()
