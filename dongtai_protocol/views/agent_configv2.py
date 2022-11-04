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
from dongtai_web.systemmonitor.data_gather import get_data_gather_data


class AgentConfigAllinOneView(OpenApiEndPoint):

    def post(self, request):
        data = get_data_gather_data()
        return R.success(data=data)
