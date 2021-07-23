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
from dongtai.models.hook_type import HookType
from dongtai.models.hook_strategy import HookStrategy

class StrategyDelete(UserEndPoint):

    def delete(self, request,id_):
        '''
        用户删除策略
        '''
        hook_type = HookType.objects.filter(pk=id_).first()
        strategy = IastStrategyModel.objects.filter(hook_type=hook_type.id).first()
        hook_strategies = hook_type.strategies.all()
        for hook_strategy in hook_strategies:
            hook_strategy.delete()
        strategy.delete()
        hook_type.delete()
        return R.success(data={"id": id_})
