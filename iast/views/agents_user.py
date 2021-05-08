#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:23
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.agent import AgentEndPoint
from dongtai_models.models.agent import IastAgent

"""
获取用户agent ID token
"""


class UserAgentList(AgentEndPoint):
    def get(self, request: Request):
        user = request.user
        if user.is_talent_admin():
            queryset = IastAgent.objects.all()
        else:
            queryset = IastAgent.objects.filter(user=user)
        queryset_datas = queryset.values("id", "token")
        data = []
        if queryset_datas:
            for item in queryset_datas:
                data.append({
                    "id": item['id'],
                    "name": item['token']
                })
        return R.success(data=data)
