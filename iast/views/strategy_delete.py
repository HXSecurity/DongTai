#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
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
from django.utils.translation import gettext_lazy as _

class StrategyDelete(UserEndPoint):

    def delete(self, request, id_):
        hook_type = HookType.objects.filter(pk=id_).first()
        if not hook_type:
            return R.failure(msg=_('This strategy does not exist'))
        hook_strategies = hook_type.strategies.all()
        for hook_strategy in hook_strategies:
            hook_strategy.enable = const.DELETE
            hook_strategy.save()
        hook_type.enable = const.DELETE
        hook_type.save()
        return R.success(data={"id": id_})
