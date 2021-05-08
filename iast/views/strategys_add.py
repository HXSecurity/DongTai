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


# 用户新增策略
class StrategyAdd(UserEndPoint):

    def post(self, request: Request):
        # 获取策略ID，str
        ids = request.data.get("ids", None)
        # 策略名称
        name = request.data.get("name", None)
        user = request.user
        if not ids or not name:
            return R.failure(msg='参数错误')
        new_strage = IastStrategyUser.objects.create(
            name=name,
            content=ids,
            user=user,
            status=1
        )
        return R.success(data={"id": new_strage.id})
