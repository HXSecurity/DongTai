#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午3:00
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.strategy_user import IastStrategyUser
from dongtai.models.strategy import IastStrategyModel


class StrategyDelete(UserEndPoint):

    def post(self, request):
        '''
        用户删除策略
        '''
        id_ = request.data.get("id", None)
        strategy = IastStrategyModel.objects.filter(
            pk=id_, user_id=request.user.id).first()
        strategy.delete()
        return R.success(data={"id": id_})
