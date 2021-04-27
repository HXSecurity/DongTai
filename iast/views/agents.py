#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:23
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.agent import AgentEndPoint
from iast.serializers.agent import AgentSerializer

"""
agent唯一标识、Agent名称、服务器地址、服务器负载、运行状态
"""


class AgentList(AgentEndPoint):
    name = "api-v1-agents"
    description = "agent列表"

    def get(self, request: Request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 20)

        queryset = self.get_auth_agents_with_user(request.user).filter(is_running=1).order_by("-latest_time")
        summery, queryset = self.get_paginator(queryset, page=page, page_size=page_size)

        return R.success(
            data=AgentSerializer(queryset, many=True).data,
            page=summery
        )
