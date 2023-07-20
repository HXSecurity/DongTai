#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.agent import AgentInstallArgsSerializer


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("The installation is complete")), ""),
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


class AgentInstall(UserEndPoint):
    name = "api-v1-agent-install"
    description = _("Installing an Agent")

    @extend_schema_with_envcheck(
        request=AgentInstallArgsSerializer,
        tags=[_("Agent")],
        summary=_("Agent Install"),
        description=_("Install the running agent by specifying the id."),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        agent_id = request.data.get("id")
        agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
        if agent:
            if agent.control != 1 and agent.is_control == 0:
                agent.control = 1
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save(update_fields=["latest_time", "control", "is_control"])
                return R.success(msg=_("The installation is complete"))
            else:
                return R.failure(
                    msg=_(
                        "The engine is being installed or uninstalled, please try again later"
                    )
                )
        else:
            return R.failure(msg=_("Engine does not exist or no permission to access"))
