#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:29
# software: PyCharm
# project: lingzhi-webapi
import time

from base import R
from iast.base.agent import AgentEndPoint
from dongtai_models.models.agent import IastAgent


class AgentUninstall(AgentEndPoint):
    name = "api-v1-agent-uninstall"
    description = "卸载agent"

    def post(self, request):
        agent_id = request.data.get('id')
        agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
        if agent:
            if agent.control != 2 and agent.is_control == 0:
                agent.control = 2
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save(update_fields=['latest_time', 'control', 'is_control'])
                return R.success(msg='正在卸载...')
            else:
                return R.failure(msg='agent正在被安装或卸载，请稍后再试')
        else:
            return R.failure(msg='引擎不存在或无权操作')
