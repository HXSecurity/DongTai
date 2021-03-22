#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午3:00
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.user import UserEndPoint
from iast.models.strategy import IastStrategyModel
from iast.serializers.strategy import StrategySerializer


class StrategyEndpoint(UserEndPoint):

    def get(self, request: Request):
        queryset = IastStrategyModel.objects.all()
        return R.success(data=StrategySerializer(queryset, many=True).data)
