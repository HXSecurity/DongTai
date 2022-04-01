from dongtai.endpoint import (UserEndPoint, R)
from django.utils.translation import gettext_lazy as _
from dongtai.models.agent import IastAgent
from iast.views.utils.commonstats import get_summary_by_agent_ids
from dongtai.models.project_version import IastProjectVersion

class AgentSummary(UserEndPoint):
    name = "api-v1-agent-summary-<id>"
    description = _("Item details - Summary")

    def get(self, request, pk):
        agent = IastAgent.objects.filter(pk=pk).only(
            'server__ip', 'server__container', 'bind_project_id',
            'project_version_id', 'language', 'token').first()
        project_version = IastProjectVersion.objects.filter(
            project_id=agent.project_version_id,
            current_version=1).only('project__name', 'version_name').first()
        data = get_summary_by_agent_ids([agent.id])
        data['ip'] = agent.server.ip
        data['middleware'] = agent.server.container
        data['project_name'] = project_version.project.name
        data['version_name'] = project_version.version_name
        data['token'] = agent.token
        data['language'] = agent.language
        return R.success(data=data)
