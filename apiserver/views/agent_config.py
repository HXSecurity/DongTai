from dongtai.endpoint import OpenApiEndPoint, R
from dongtai.models.agent_config import IastAgentConfig
from django.db.models import Q


class AgentConfigView(OpenApiEndPoint):

    def get(self, request):
        agent_id = request.data.get('agentId', None)
        agent = IastAgent.objects.filter(pk=agent_id).first()
        server = agent.server
        q = Q(cluster_name__in=('', server.cluster_name)) | Q(
            cluster_version__in=('', server.cluster_version)) | Q(
                hostname__in=('', server.hostname)) | Q(
                    ip__in=('', server.cluster_ip))
        config = IastAgentConfig.objects.filter(Q(
            user__in=users) & q).order_by('-priority').first()
        data = config.details
        return R.success(data=data)
