#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vul_level import IastVulLevel



class StrategyType(UserEndPoint):

    def get(self, request):
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
