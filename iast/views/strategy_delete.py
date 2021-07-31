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
from dongtai.utils import const

class StrategyDelete(UserEndPoint):

    def delete(self, request, id_):
        '''
        用户删除策略
        '''
        hook_type = HookType.objects.filter(pk=id_).first()
        if not hook_type:
            return R.failure(msg='该策略不存在')
        hook_strategies = hook_type.strategies.all()
        for hook_strategy in hook_strategies:
            hook_strategy.enable = const.DELETE
            hook_strategy.save()
        hook_type.enable = const.DELETE
        hook_type.save()
        return R.success(data={"id": id_})
