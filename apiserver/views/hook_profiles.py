#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:16
# software: PyCharm
# project: lingzhi-webapi
import json
import logging

from django.http import JsonResponse
from rest_framework.request import Request

from AgentServer.base import R
from AgentServer import const
from apiserver.base.openapi import OpenApiEndPoint
from apiserver.models.hook_talent_strategy import IastHookTalentStrategy
# note: 当前依赖必须保留，否则无法通过hooktype反向查找策略
from apiserver.models.hook_strategy import HookStrategy
from apiserver.models.hook_type import HookType

logger = logging.getLogger("django")


class HookProfilesEndPoint(OpenApiEndPoint):
    name = "api-v1-profiles"
    description = "获取HOOK策略"

    @staticmethod
    def get_profiles(talent, user=None):
        profiles = list()
        talent_strategy = IastHookTalentStrategy.objects.filter(talent=talent).first()
        strategy_types = json.loads(talent_strategy.values)
        enable_hook_types = HookType.objects.filter(id__in=strategy_types, enable=const.HOOK_TYPE_ENABLE)
        for enable_hook_type in enable_hook_types:
            strategy_details = list()
            profiles.append({
                'type': enable_hook_type.type,
                'enable': enable_hook_type.enable,
                'value': enable_hook_type.value,
                'details': strategy_details
            })
            strategies = enable_hook_type.strategies.filter(created_by__in=[1, user.id] if user else [1])
            for strategy in strategies:
                strategy_details.append({
                    "source": strategy.source,
                    "track": strategy.track,
                    "target": strategy.target,
                    "value": strategy.value,
                    "inherit": strategy.inherit
                })
        return profiles

    def get(self, request: Request):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        user = request.user
        talent = user.get_talent()
        profiles = self.get_profiles(talent, user)

        return JsonResponse(R.success(data=profiles))


if __name__ == '__main__':
    strategy_count = HookStrategy.objects.count()
