from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_web.views.utils.commonstats import get_summary_by_agent_ids


class AgentSummary(UserEndPoint):
    name = "api-v1-agent-summary-<id>"
    description = _("Item details - Summary")

    @extend_schema(
        tags=[_("Agent")],
        summary="探针数量统计",
        deprecated=True,
    )
    def get(self, request, pk):
        try:
            pk = int(pk)
        except Exception:
            return R.failure()
        agent = (
            IastAgent.objects.filter(pk=pk)
            .only(
                "server__ip",
                "server__container",
                "bind_project_id",
                "language",
                "token",
            )
            .first()
        )
        if not agent:
            return R.failure()
        project_version = (
            IastProjectVersion.objects.filter(
                project_id=agent.bind_project_id, current_version=1
            )
            .only("project__name", "version_name")
            .first()
        )
        data = get_summary_by_agent_ids([agent.id])
        data["ip"] = agent.server.ip
        data["middleware"] = agent.server.container
        data["project_name"] = project_version.project.name if project_version else ""
        data["version_name"] = project_version.version_name if project_version else ""
        data["token"] = agent.token
        data["language"] = agent.language
        return R.success(data=data)
