#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/6/3 11:36
# software: PyCharm
# project: webapi

from dongtai.models.deploy import IastDeployDesc

from base import R
from iast.base.agent import AgentEndPoint


class AgentDeployDesc(AgentEndPoint):
    """
    IAST部署说明
    """
    name = "api-v1-iast-deploy-desc"
    description = "Agent部署文档"

    def get(self, request):
        queryset = IastDeployDesc.objects.all()

        os = request.query_params.get('os', 'linux')
        if os:
            queryset = queryset.filter(os=os)

        middle = request.query_params.get('server', 'tomcat')
        if middle:
            queryset = queryset.filter(middleware=middle)

        queryset = queryset.last()
        if queryset:
            return R.success(desc=queryset.desc)
        else:
            return R.failure(desc='暂无数据')
