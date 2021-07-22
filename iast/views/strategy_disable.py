#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 下午3:34
# software: PyCharm
# project: lingzhi-webapi
from dongtai.models.hook_type import HookType
from dongtai.models.hook_strategy import HookStrategy
from dongtai.utils import const

from dongtai.endpoint import R
from dongtai.endpoint import TalentAdminEndPoint


class StrategyDisableEndpoint(TalentAdminEndPoint):
    def get(self, request, id):
        strategy_model = HookType.objects.filter(id=id).first()
        if strategy_model:
            counts = strategy_model.strategies.filter(enable=const.HOOK_TYPE_ENABLE).update(
                enable=const.HOOK_TYPE_DISABLE)
            strategy_model.enable = const.HOOK_TYPE_DISABLE
            strategy_model.save(update_fields=['enable'])

            return R.success(msg=f'策略禁用成功，共{counts}条hook规则')
        else:
            return R.failure(status=202, msg='策略不存在')


if __name__ == '__main__':
    # 增加HookStrategy调用，确保关联关系存在
    HookStrategy.objects.values("id").count()
