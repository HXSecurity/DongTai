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
from iast.utils import get_model_field
from dongtai.models.agent import IastAgent
from functools import reduce
from django.db.models import Q

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

            fields = get_model_field(
                IastAgent,
                include=['token', 'project_name'],
            )
            searchfields = dict(
                filter(lambda k: k[0] in fields, request.query_params.items()))
            searchfields_ = {k: v for k, v in searchfields.items() if k in fields}
            q = reduce(
                lambda x, y: x | y,
                map(
                    lambda x: Q(**x),
                    map(
                        lambda kv_pair:
                        {'__'.join([kv_pair[0], 'icontains']): kv_pair[1]},
                        searchfields_.items())), Q())
            q = q & Q(is_running=running_state)
            queryset = IastAgent.objects.filter(q).order_by('-latest_time').all()
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
