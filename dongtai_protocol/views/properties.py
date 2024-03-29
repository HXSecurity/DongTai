#!/usr/bin/env python
# datetime:2020/5/21 15:56
import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_properties import IastAgentProperties
from dongtai_common.utils.request_type import Request
from dongtai_protocol.serializers.agent_properties import AgentPropertiesSerialize

logger = logging.getLogger("django")


class PropertiesEndPoint(OpenApiEndPoint):
    """
    当前用户详情
    """

    name = "api-v1-properties"
    description = "获取属性配置"

    @extend_schema(
        summary="获取属性配置",
        tags=[_("Profile")],
    )
    def get(self, request: Request):
        """
        IAST下载 agent接口
        :param request:
        :return:{
            "status": 201,
            "data":{
                "hook_type": 0,
                "dump_class": 0
            },
            "msg": "success"
        }
        """
        agent_token = request.query_params.get("agentName", None)
        agent = IastAgent.objects.filter(token=agent_token).first()
        if agent:
            queryset = IastAgentProperties.objects.filter(agent=agent).first()
            if queryset:
                return R.success(AgentPropertiesSerialize(queryset).data)
        return R.failure(data=None)
