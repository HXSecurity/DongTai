#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/4 16:47
# software: PyCharm
# project: webapi
import logging
import time

from dongtai.models.agent import IastAgent

from dongtai.endpoint import OpenApiEndPoint, R
from drf_spectacular.utils import extend_schema

from apiserver.api_schema import DongTaiParameter

logger = logging.getLogger("django")


class EngineUpdateEndPoint(OpenApiEndPoint):
    name = "iast_engine_update_status_edit"
    description = "IAST 检测引擎更新状态修改接口"

    def get(self, request, status=None):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        agent_name = request.query_params.get('agent_name')
        agent = IastAgent.objects.filter(user=request.user, token=agent_name, is_running=1).first()
        if not agent:
            return R.failure("agent不存在或无权限访问")

        if status:
            if agent.is_control == 1:
                agent.control = status
                agent.is_control = 0
                agent.latest_time = int(time.time())
                agent.save()
                return R.success(msg="安装完成")
            else:
                return R.failure(msg="引擎正在被安装或卸载，请稍后再试")
        else:
            if agent.control == 1 and agent.is_control == 0:
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save()
                return R.success(data=agent.control)
            else:
                return R.failure(msg="不需要更新或正在更新中")


class EngineAction(OpenApiEndPoint):
    name = "iast_engine_update_status_edit"
    description = "IAST 检测引擎更新状态修改接口"

    @extend_schema(
        description='Check Agent Engine Control Code',
        parameters=[
            DongTaiParameter.AGENT_NAME,
        ],
        responses=R,
        methods=['GET']
    )
    def get(self, request):
        agent_id = request.query_params.get('agentId')
        agent = IastAgent.objects.filter(user=request.user, pk=agent_id, is_running=1).first()
        if not agent:
            return R.failure("agent不存在或无权限访问")

        if agent.is_control == 0:
            return R.failure(msg="暂无命令", data="notcmd")

        # coreRegisterStart
        if agent.control == 2:
            agent.is_control = 0
            agent.is_core_running = 1
            agent.latest_time = int(time.time())
            agent.save(update_fields=['is_control', 'is_core_running', 'latest_time'])
            return R.success(data="coreRegisterStart", msg=str(agent.is_running) + agent.token)

        # coreStart
        if agent.control == 3:
            agent.is_control = 0
            agent.is_core_running = 1
            agent.latest_time = int(time.time())
            agent.save(update_fields=['is_control', 'is_core_running', 'latest_time'])
            return R.success(data="coreStart", msg=str(agent.is_running) + agent.token)

        # coreStop
        if agent.control == 4:
            agent.is_control = 0
            agent.is_core_running = 0
            agent.latest_time = int(time.time())
            agent.save(update_fields=['is_control', 'is_core_running', 'latest_time'])
            return R.success(data="coreStop")
        return R.success(data="notcmd")
