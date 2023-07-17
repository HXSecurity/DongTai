from dongtai_protocol.decrypter import parse_data
from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_config import IastAgentConfig
from django.db.models import Q
from drf_spectacular.utils import extend_schema
import logging
from dongtai_common.utils.systemsettings import get_circuit_break
from django.utils.translation import gettext_lazy as _
from result import Ok, Err, Result
from dongtai_common.models.agent_config import MetricGroup
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.common import get_data_gather_data
from dongtai_common.models.project import IastProject

class _AgentConfigArgsSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField(required=True, help_text=_('Agent id'))


def get_agent_data_gather_config(agent_id):
    config = get_data_gather_data()
    return config


class AgentConfigAllinOneView(OpenApiEndPoint):

    @extend_schema_with_envcheck(
        [_AgentConfigArgsSerializer],
        summary="agent配置",
        tags=['Agent服务端交互协议'],
        methods=['GET'])
    def get(self, request):
        ser = _AgentConfigArgsSerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError as e:
            return R.failure(data=e.detail)
        agent = IastAgent.objects.filter(pk=ser.data['agent_id']).first()
        if not agent:
            return R.failure(msg="No agent found.")
        data = get_agent_data_gather_config(ser.data['agent_id'])
        if agent.bind_project is not None and agent.bind_project.enable_log is not None:
            data['enable_log'] = agent.bind_project.enable_log
        if agent.bind_project is not None and agent.bind_project.log_level is not None:
            data['log_level'] = agent.bind_project.log_level
        return R.success(data=data)
