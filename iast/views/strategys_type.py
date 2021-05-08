#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午3:00
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.strategy import IastStrategyModel
from dongtai_models.models.vul_level import IastVulLevel


# 按高中低分类策略
class StrategyType(UserEndPoint):

    def get(self, request: Request):
        queryset = IastStrategyModel.objects.all()
        allType = IastVulLevel.objects.all().order_by("id")
        result = []
        curTyp = {}
        if queryset:
            for item in queryset:
                if item.level.id not in curTyp.keys():
                    curTyp[item.level_id] = []
                curTyp[item.level_id].append({
                    "strategy_id": item.id,
                    "level_id": item.level_id,
                    "vul_name": item.vul_name
                })
        if allType:
            for item in allType:
                result.append({
                    "level_id": item.id,
                    "level_name": item.name_type,
                    "type_value": curTyp.get(item.id, [])
                })
        return R.success(data=result)
