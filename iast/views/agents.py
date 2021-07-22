#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:23
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R

from dongtai.utils import const
from iast.serializers.agent import AgentSerializer

logger = logging.getLogger('dongtai-webapi')
"""
agent唯一标识、Agent名称、服务器地址、服务器负载、运行状态
"""


class AgentList(UserEndPoint):
    name = "api-v1-agents"
    description = "agent列表"

    def get(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('pageSize', 20))
            running_state = int(request.query_params.get('state', const.RUNNING))

            queryset = self.get_auth_agents_with_user(request.user).filter(is_running=running_state).order_by(
                "-latest_time")
            summery, queryset = self.get_paginator(queryset, page=page, page_size=page_size)

            return R.success(
                data=AgentSerializer(queryset, many=True).data,
                page=summery
            )
        except ValueError as e:
            logger.error(e)
            return R.failure(msg=f'参数格式不正确，请检查。错误信息：{e}')
        except Exception as e:
            logger.error(e)
            return R.failure(msg=str(e))
