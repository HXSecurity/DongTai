
import logging
import time

from dongtai.models.agent import IastAgent
from dongtai.endpoint import OpenApiEndPoint, R
from apiserver.decrypter import parse_data
from drf_spectacular.utils import extend_schema
from dongtai.models.server import IastServer
from django.utils.translation import gettext_lazy as _
logger = logging.getLogger('dongtai.openapi')


class AgentUpdateEndPoint(OpenApiEndPoint):
    @extend_schema(
        description='Agent Update, Data is Gzip',
        responses=[
            {204: None}
        ],
        methods=['POST'])
    def post(self, request):
        try:
            param = parse_data(request.read())
            agent_id = int(param.get('agentId', None))
            server_addr = param.get('serverAddr', None)
            server_port = int(param.get('serverPort', None))
        except Exception as e:
            return R.failure(msg="参数错误")
        user = request.user
        # server_port = param.get('serverPort')
        # server_path = param.get('serverPath')
        # server_env = param.get('serverEnv')
        agent = IastAgent.objects.filter(id=agent_id, user=user).first()
        if not agent:
            return R.failure(msg="agent no register")
        else:
            server = IastServer.objects.filter(id=agent.server_id).first()
            if not server:
                return R.failure(msg="agent no register")
            else:
                server.ip = server_addr
                server.port = server_port
                server.update_time = int(time.time())
                server.save(update_fields=['ip',  'update_time'])
        logger.info(_('Server record update success'))
        return R.success(msg="success update")
