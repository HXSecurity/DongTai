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


class _AgentConfigArgsSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField(required=True, help_text=_('Agent id'))


def get_agent_data_gather_config(agent_id):
    config = get_data_gather_data()
    return config


class AgentConfigAllinOneView(OpenApiEndPoint):

    @extend_schema_with_envcheck(
        [_AgentConfigArgsSerializer],
        tags=['agent upload'],
        description='Through agent_ Id get data gather strategy',
        methods=['GET'])
    def get(self, request):
        ser = _AgentConfigArgsSerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError as e:
            return R.failure(data=e.detail)
        data = get_agent_data_gather_config(ser.agent_id)
        return R.success(data=data)
