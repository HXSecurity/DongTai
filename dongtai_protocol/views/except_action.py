import logging
import time
from urllib.parse import urlparse, urlunparse

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ViewSet

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.server import IastServer
from dongtai_common.utils.const import OPERATE_PUT
from dongtai_protocol.decrypter import parse_data
from dongtai_web.views.project_add import is_ip

logger = logging.getLogger("dongtai.openapi")

EVENT_MAPPING = {1: "加载成功", 2: "降级成功", 3: "卸载成功", 4: "代码异常"}


class AgentActionV2EndPoint(OpenApiEndPoint, ViewSet):
    @extend_schema(
        description="Agent Update, Data is Gzip",
        responses=[{204: None}],
        tags=["Agent服务端交互协议", OPERATE_PUT],
        summary="agent实际状态",
        methods=["POST"],
    )
    def actual_running_status(self, request):
        try:
            param = parse_data(request.read())
            agent_id = int(param.get("agentId", None))
            actual_running_status = int(param.get("actualRunningStatus", None))
            state_status = int(param.get("stateStatus", None))
        except Exception as exception:
            logger.error(exception, exc_info=True)
            return R.failure(msg="参数错误")
        agent = IastAgent.objects.filter(pk=agent_id).first()
        if not agent:
            return R.failure(msg=_("Agent not found"))
        if (
            agent.only_register()
            or agent.actual_running_status != actual_running_status
        ):
            if not agent.events:
                agent.append_events("注册成功")
            if actual_running_status in EVENT_MAPPING:
                agent.append_events(EVENT_MAPPING[actual_running_status])
        agent.actual_running_status = actual_running_status
        agent.state_status = state_status
        agent.save()
        return R.success(msg="success update")

    @extend_schema(
        description="Agent Update, Data is Gzip",
        responses=[{204: None}],
        tags=[_("Agent服务端交互协议")],
        summary="agent期望状态",
        methods=["GET"],
    )
    def except_running_status(self, request):
        if "agentId" not in request.GET.keys():
            return R.failure()
        agent_id = request.GET["agentId"]
        agent = IastAgent.objects.filter(pk=agent_id).first()
        if not agent:
            return R.failure(msg=_("Agent not found"))
        data = {
            "exceptRunningStatus": agent.except_running_status,
            "allowReport": agent.allow_report,
        }
        return R.success(msg="success update", data=data)
