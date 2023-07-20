#!/usr/bin/env python
# datetime:2020/8/4 16:47
import logging
import time

from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_protocol.api_schema import DongTaiParameter

logger = logging.getLogger("django")


class EngineUpdateEndPoint(OpenApiEndPoint):
    name = "iast_engine_update_status_edit"
    description = "IAST 检测引擎更新状态修改接口"

    @extend_schema(
        summary="IAST 检测引擎更新状态修改接口",
        tags=["Agent服务端交互协议"],
    )
    def get(self, request, status=None):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        agent_name = request.query_params.get("agent_name")
        agent = IastAgent.objects.filter(
            user=request.user, token=agent_name, is_running=1
        ).first()
        if not agent:
            return R.failure("agent不存在或无权限访问")

        if status:
            if agent.is_control == 1:
                agent.control = status
                agent.is_control = 0
                agent.latest_time = int(time.time())
                agent.save()
                return R.success(msg="安装完成")
            return R.failure(msg="引擎正在被安装或卸载,请稍后再试")
        if agent.control == 1 and agent.is_control == 0:
            agent.is_control = 1
            agent.latest_time = int(time.time())
            agent.save()
            return R.success(data=agent.control)
        return R.failure(msg="不需要更新或正在更新中")


class EngineAction(OpenApiEndPoint):
    name = "iast_engine_update_status_edit"
    description = "IAST 检测引擎更新状态修改接口"

    @extend_schema(
        description="Check Agent Engine Control Code",
        parameters=[
            DongTaiParameter.AGENT_NAME,
        ],
        responses=R,
        methods=["GET"],
        summary="检查 Agent Engine 状态",
        tags=["Agent服务端交互协议"],
        deprecated=True,
    )
    def get(self, request):
        agent_id = request.query_params.get("agentId")
        agent = IastAgent.objects.filter(
            user=request.user, pk=agent_id, is_running=1
        ).first()
        if not agent:
            return R.failure("agent不存在或无权限访问")
        agent_status = {
            0: {
                "key": "无下发指令",
                "value": "notcmd",
            },
            2: {
                "key": "注册启动引擎",
                "value": "coreRegisterStart",
            },
            3: {
                "key": "开启引擎核心",
                "value": "coreStart",
            },
            4: {
                "key": "关闭引擎核心",
                "value": "coreStop",
            },
            5: {
                "key": "卸载引擎核心",
                "value": "coreUninstall",
            },
            6: {
                "key": "强制开启引擎核心性能熔断",
                "value": "corePerformanceForceOpen",
            },
            7: {
                "key": "强制关闭引擎核心性能熔断",
                "value": "corePerformanceForceClose",
            },
            8: {
                "key": "Agent升级",
                "value": "update",
            },
        }
        if agent.is_control == 0:
            return R.failure(msg="暂无命令", data="notcmd")
        agent.is_control = 0
        agent.latest_time = int(time.time())
        if agent.control in [4, 5, 6]:
            agent.is_core_running = 0
        else:
            agent.is_core_running = 1
        if agent.control == 8:
            if cache.get(f"agent_update_{agent_id}", False):
                agent.is_control = 0
                agent.control = 2
                cache.delete(f"agent_update_{agent_id}")
            else:
                cache.set(f"agent_update_{agent_id}", True, 60 * 5)
                agent.is_control = 1
                agent.control = 5
        agent.save(update_fields=["is_control", "is_core_running", "latest_time"])
        result_cmd = agent_status.get(
            agent.control, {"key": "无下发指令", "value": "notcmd"}
        ).get("value")
        return R.success(data=result_cmd)
