#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 下午3:34
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.user import TalentAdminEndPoint
from iast.const import STRATEGY_DISABLE
from dongtai_models.models.strategy import IastStrategyModel


class StrategyDisableEndpoint(TalentAdminEndPoint):
    def get(self, request: Request, id):
        strategy = IastStrategyModel.objects.filter(id=id)
        if strategy and len(strategy) > 0:
            strategy[0].state = STRATEGY_DISABLE
            strategy[0].save(update_fields=['state'])
            return R.success()
        else:
            return R.failure(status=202, msg='策略不存在')
