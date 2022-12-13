import logging
import time

from dongtai_common.models.agent import IastAgent
from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_protocol.decrypter import parse_data
from drf_spectacular.utils import extend_schema
from dongtai_common.models.server import IastServer
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse, urlunparse
from dongtai_web.views.project_add import is_ip
from rest_framework.viewsets import ViewSet
logger = logging.getLogger('dongtai.openapi')


class AgentActionV2EndPoint(OpenApiEndPoint,ViewSet):

    @extend_schema(description='Agent Update, Data is Gzip',
                   responses=[{
                       204: None
                   }],
                   methods=['POST'])
    def actual_running_status(self, request):
        try:
            param = parse_data(request.read())
            agent_id = int(param.get('agentId', None))
            actual_running_status = int(param.get('actualRunningStatus', None))
            state_status = int(param.get('stateStatus', None))
        except Exception as e:
            logger.error(e, exc_info=True)
            return R.failure(msg="参数错误")
        agent = IastAgent.objects.filter(pk=agent_id).first()
        if not agent:
            return R.failure(msg=_("Agent not found"))
        agent.actual_running_status = actual_running_status
        agent.state_status = state_status
        agent.save()
        return R.success(msg="success update")

    @extend_schema(description='Agent Update, Data is Gzip',
                   responses=[{
                       204: None
                   }],
                   methods=['POST'])
    def except_running_status(self, request):
        if 'agentId' not in request.GET.keys():
            return R.failure()
        agent_id = request.GET['agentId']
        agent = IastAgent.objects.filter(pk=agent_id).first()
        if not agent:
            return R.failure(msg=_("Agent not found"))
        data = {"exceptRunningStatus": agent.except_running_status}
        return R.success(msg="success update", data=data)
