from apiserver.decrypter import parse_data
from dongtai.endpoint import OpenApiEndPoint, R
from dongtai.models.agent import IastAgent
from dongtai.models.agent_config import IastAgentConfig
from django.db.models import Q
from drf_spectacular.utils import extend_schema


class AgentConfigView(OpenApiEndPoint):

    @extend_schema(
        description='Through agent_ Id get disaster recovery strategy',
        responses=R,
        methods=['POST']
    )
    def post(self, request):
        # agent_id = request.data.get('agentId', None)
        param = parse_data(request.read())
        agent_id = param.get('agentId')

        user = request.user
        agent = IastAgent.objects.filter(pk=agent_id).first()
        if agent and agent.server_id:
            server = agent.server

            if server:

                config = IastAgentConfig.objects.filter(
                    user=user,
                    cluster_name__in=('', server.cluster_name),
                    cluster_version__in=('', server.cluster_version),
                    hostname__in=('', server.hostname),
                    ip__in=('', server.ip)
                ).order_by('-priority').first()
                if config:
                    data = config.details
                else:
                    data = {}
            else:
                data = {}
        else:
            data = {}

        return R.success(data=data)
