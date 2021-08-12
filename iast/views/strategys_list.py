#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.strategy_user import IastStrategyUser


class StrategyList(UserEndPoint):

    def get(self, request):
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
