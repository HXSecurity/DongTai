#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time
from dongtai.endpoint import UserEndPoint, R

from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _


class AgentStart(UserEndPoint):
    name = "api-v1-agent-start"
    description = _("Start Agent")

    def post(self, request):
        agent_id = request.data.get('id')
        agent_ids = request.data.get('ids', None)
        if agent_ids:
            agent_ids = agent_ids.split(',')
        if agent_id:
            agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
            if agent is None:
                return R.failure(msg=_('Engine does not exist or no permission to access'))
            if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
                return R.failure(msg=_('Agent is stopping service, please try again later'))
            agent.control = 3
            agent.is_control = 1
            agent.latest_time = int(time.time())
            agent.save(update_fields=['latest_time', 'control', 'is_control'])
        if agent_ids:
            for agent_id in agent_ids:
                agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
                if agent is None:
                    continue
                if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
                    continue
                agent.control = 3
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save(update_fields=['latest_time', 'control', 'is_control'])
        return R.success(msg=_('Starting…'))
