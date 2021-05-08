#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 下午3:32
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.user import TalentAdminEndPoint
from iast.const import STRATEGY_ENABLE
from dongtai_models.models.strategy import IastStrategyModel


class StrategyEnableEndpoint(TalentAdminEndPoint):
    def get(self, request: Request, id):
        strategy = IastStrategyModel.objects.filter(id=id)
        if strategy and len(strategy) > 0:
            strategy[0].state = STRATEGY_ENABLE
            strategy[0].save(update_fields=['state'])

            return R.success(msg='success')
        else:
            return R.failure(msg='策略不存在')
