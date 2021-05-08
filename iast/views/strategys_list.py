#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午3:00
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.strategy_user import IastStrategyUser


# 用户获取自有策略列表
class StrategyList(UserEndPoint):

    def get(self, request: Request):
        user = request.user
        queryset = IastStrategyUser.objects.filter(
            user=user,
            status=1
        ).values("id", "name").order_by("-id")
        data = []
        if queryset:
            for item in queryset:
                data.append({
                    "id": item['id'],
                    "name": item['name'],
                })
        return R.success(data=data)
