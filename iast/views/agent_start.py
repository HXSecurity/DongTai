#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:29
# software: PyCharm
# project: lingzhi-webapi
import time
from dongtai.endpoint import UserEndPoint, R

from dongtai.models.agent import IastAgent


class AgentStart(UserEndPoint):
    name = "api-v1-agent-start"
    description = "启动agent"

    def post(self, request):
        agent_id = request.data.get('id')
        agent_ids = request.data.get('ids', None)
        if agent_ids:
            agent_ids = agent_ids.split(',')
        if agent_id:
            agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
            if agent is None:
                return R.failure(msg='引擎不存在或无权操作')
            if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
                return R.failure(msg='agent正在进行非启动停止操作，请稍后再试')
            agent.control = 3
            agent.is_control = 1
            agent.latest_time = int(time.time())
            agent.save(update_fields=['latest_time', 'control', 'is_control'])
        if agent_ids:
            for agent_id in agent_ids:
                agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
                if agent is None:
                    continue
#                    return R.failure(msg='引擎不存在或无权操作')
                if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
                    continue
#                    return R.failure(msg='agent正在进行非启动停止操作，请稍后再试')
                agent.control = 3
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save(update_fields=['latest_time', 'control', 'is_control'])
        return R.success(msg='正在启动...')
