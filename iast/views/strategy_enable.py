#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 下午3:32
# software: PyCharm
# project: lingzhi-webapi
from dongtai.models.hook_type import HookType
from dongtai.models.hook_strategy import HookStrategy
from dongtai.utils import const

from base import R
from iast.base.user import TalentAdminEndPoint


class StrategyEnableEndpoint(TalentAdminEndPoint):
    def get(self, request, id):
        strategy_model = HookType.objects.filter(id=id).first()
        if strategy_model:
            counts = strategy_model.strategies.filter(enable=const.HOOK_TYPE_DISABLE).update(
                enable=const.HOOK_TYPE_ENABLE)
            strategy_model.enable = const.HOOK_TYPE_ENABLE
            strategy_model.save(update_fields=['enable'])

            return R.success(msg=f'策略启用成功，共{counts}条hook规则')
        else:
            return R.failure(msg='策略不存在')


if __name__ == '__main__':
    # 增加HookStrategy调用，确保关联关系存在
    HookStrategy.objects.values("id").count()
