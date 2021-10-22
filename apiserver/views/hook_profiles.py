#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:16
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request

from dongtai.utils import const
from dongtai.endpoint import OpenApiEndPoint, R

# note: 当前依赖必须保留，否则无法通过hooktype反向查找策略
from apiserver.api_schema import DongTaiParameter

logger = logging.getLogger("django")
JAVA = 1
LANGUAGE_DICT= {'JAVA':1,'PYTHON':2,'PHP':3,'G0':4}
                
class HookProfilesEndPoint(OpenApiEndPoint):
    name = "api-v1-profiles"
    description = "获取HOOK策略"

    @staticmethod
    def get_profiles(user=None, language_id=JAVA):
        profiles = list()
        hook_types = HookType.objects.filter(language_id=language_id).all()
        for hook_type in hook_types:
            strategy_details = list()
            profiles.append({
                'type': hook_type.type,
                'enable': hook_type.enable,
                'value': hook_type.value,
                'details': strategy_details
            })
            strategies = hook_type.strategies.filter(
                created_by__in=[1, user.id] if user else [1],
                enable=const.HOOK_TYPE_ENABLE)
            for strategy in strategies:
                strategy_details.append({
                    "source": strategy.source,
                    "track": strategy.track,
                    "target": strategy.target,
                    "value": strategy.value,
                    "inherit": strategy.inherit
                })
        return profiles

    @extend_schema(
        description='Pull Agent Engine Hook Rule',
        parameters=[
            DongTaiParameter.LANGUAGE,
        ],
        responses=R,
        methods=['GET']
    )
    def get(self, request):
        user = request.user

        language = request.query_params.get('language')
        language_id = LANGUAGE_DICT.get(language,None) if language is not None else None
        language_id = JAVA if language_id is None and language is None else language_id
        profiles = self.get_profiles(user, language_id)

        return R.success(data=profiles)

    def put(self, request):
        pass

    def post(self):
        pass


if __name__ == '__main__':
    strategy_count = HookStrategy.objects.count()
