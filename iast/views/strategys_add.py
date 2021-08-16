#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.strategy_user import IastStrategyUser
from django.utils.translation import gettext_lazy as _



class StrategyAdd(UserEndPoint):

    def post(self, request):
        
        ids = request.data.get("ids", None)
        
        name = request.data.get("name", None)
        user = request.user
        if not ids or not name:
            return R.failure(msg=_('Parameter error'))
        new_strage = IastStrategyUser.objects.create(
            name=name,
            content=ids,
            user=user,
            status=1
        )
        return R.success(data={"id": new_strage.id})
