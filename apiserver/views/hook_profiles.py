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

from apiserver.base.openapi import OpenApiEndPoint
from apiserver.models.hook_strategy_type import IastHookStrategyType
from apiserver.models.hook_strategy_type_relation import IastHookStrategyTypeRelation
from apiserver.models.hook_talent_strategy import IastHookTalentStrategy
from user.models.department_talent import AuthDepartmentTalent
from user.models.user_department import AuthUserDepartment

logger = logging.getLogger("django")


class HookProfilesEndPoint(OpenApiEndPoint):
    name = "api-v1-profiles"
    description = "获取HOOK策略"

    @staticmethod
    def get_talent(user):
        user_department = AuthUserDepartment.objects.filter(user=user).first()
        department_talent = AuthDepartmentTalent.objects.filter(department=user_department.department).first()
        return department_talent.talent if department_talent else None

    @staticmethod
    def get_profiles(talent):
        profiles = list()
        talent_strategy = IastHookTalentStrategy.objects.filter(talent=talent).first()
        strategy_types = json.loads(talent_strategy.values)
        # fixme enable使用常量替代
        enable_strategy_types = IastHookStrategyType.objects.filter(id__in=strategy_types, enable=1)
        for enable_strategy_type in enable_strategy_types:
            strategy_details = list()
            profiles.append({
                'type': enable_strategy_type.type,
                'enable': enable_strategy_type.enable,
                'value': enable_strategy_type.value,
                'details': strategy_details
            })
            strategy_type_relations = IastHookStrategyTypeRelation.objects.filter(type=enable_strategy_type)
            for strategy_type_relation in strategy_type_relations:
                strategy_details.append({
                    "source": strategy_type_relation.strategy.source,
                    "track": strategy_type_relation.strategy.track,
                    "target": strategy_type_relation.strategy.target,
                    "value": strategy_type_relation.strategy.value,
                    "inherit": strategy_type_relation.strategy.inherit
                })
        return profiles

    def get(self, request: Request):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        # todo:
        #   1 根据用户查找租户
        #   2 根据租户，查找策略类型
        #   - 考虑是否需要用户级策略
        #   3 根据策略类型，加载对应的策略
        user = request.user
        talent = self.get_talent(user)
        profiles = self.get_profiles(talent)

        return JsonResponse({
            "status": 201,
            "msg": "策略获取成功",
            "data": profiles
        })
