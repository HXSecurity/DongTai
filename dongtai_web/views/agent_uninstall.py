#!/usr/bin/env python
import time

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_web.serializers.agent import AgentInstallArgsSerializer
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Uninstalling ...")), ""),
        (
            (
                202,
                _(
                    "The engine is being installed or uninstalled, please try again later"
                ),
            ),
            "",
        ),
        ((202, _("Engine does not exist or no permission to access")), ""),
    )
)


class AgentUninstall(UserEndPoint):
    name = "api-v1-agent-uninstall"
    description = _("Uninstall Agent")

    @extend_schema_with_envcheck(
        request=AgentInstallArgsSerializer,
        tags=[_("Agent")],
        summary=_("Agent Uninstall"),
        description=_("Uninstall the running agent by specifying the id."),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        agent_id = request.data.get("id")
        agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
        if agent:
            if agent.control != 2 and agent.is_control == 0:
                agent.control = 2
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save(update_fields=["latest_time", "control", "is_control"])
                return R.success(msg=_("Uninstalling ..."))
            return R.failure(
                msg=_(
                    "Agent is being installed or uninstalled, please try again later"
                )
            )
        return R.failure(msg=_("Engine does not exist or no permission to access"))
