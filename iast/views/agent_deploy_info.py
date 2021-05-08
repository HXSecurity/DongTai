#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/6/3 11:36
# software: PyCharm
# project: webapi

from rest_framework.request import Request

from base import R
from iast.base.agent import AgentEndPoint
from dongtai_models.models.deploy import IastDeployDesc


class AgentDeployInfo(AgentEndPoint):
    """
    IAST部署,前置选择条件
    """
    name = "api-v1-iast-deploy-info"
    description = "Agent部署文档"

    def get(self, request: Request):
        condition = {
            "agents": ["Java", ".Net Core", "C#"],
            "java_version": ["Java 1.6", "Java 1.7", "Java 1.8", "Java 9", "Java 10", "Java 11", "Java 13"],
            "middlewares": [],
            "system": ["windows", "linux"]
        }
        queryset = IastDeployDesc.objects.all()
        if queryset:

            for item in queryset:
                if item.middleware not in condition['middlewares']:
                    condition['middlewares'].append(item.middleware)
        return R.success(data=condition)
