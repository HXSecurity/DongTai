#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:29
# software: PyCharm
# project: lingzhi-webapi
import time

from base import R
from iast.base.agent import AgentEndPoint
# from iast.models.agent import IastAgent
from dongtai_models.models.agent import IastAgent


class AgentStart(AgentEndPoint):
    name = "api-v1-agent-stop"
    description = "暂停agent"

    def post(self, request):
        agent_id = request.data.get('id')
        agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
        if agent == None:
            return R.failure(msg='引擎不存在或无权操作')
        if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
            return R.failure(msg='agent正在进行非启动停止操作，请稍后再试')
        agent.control = 3
        agent.is_control = 1
        agent.latest_time = int(time.time())
        agent.save(update_fields=['latest_time', 'control', 'is_control'])
        return R.success(msg='正在启动...')
