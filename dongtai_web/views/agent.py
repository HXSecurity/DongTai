#!/usr/bin/env python


from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_web.utils import (
    extend_schema_with_envcheck,
    get_response_serializer,
)


class _AgentResponseDataAgentSerializer(serializers.ModelSerializer):
    token = serializers.CharField(help_text=_("The name of agent"))
    id = serializers.CharField(help_text=_("The id of agent"))
    version = serializers.CharField(help_text=_("The version of agent"))
    latest_time = serializers.IntegerField(
        help_text=_("The latest update time of agent")
    )
    is_running = serializers.IntegerField(help_text=_("The running status of agent"))
    is_core_running = serializers.IntegerField(
        help_text=_("The running status of agent")
    )
    control = serializers.IntegerField(
        help_text=_("agent control bit, 1-install, 2-uninstall, 0-no control")
    )
    is_control = serializers.IntegerField(
        help_text=_("Whether it is in control, 0-No, 1-Yes")
    )
    bind_project_id = serializers.IntegerField(
        help_text=_("Bundled project ID, if it exists, it will be bundled."), default=0
    )
    project_name = serializers.CharField(
        help_text=_(
            "Project name, used to start the agent first and then create the project"
        )
    )
    online = serializers.IntegerField(
        help_text=_(
            "1 is running online, 0 is not running, same token, only one online"
        )
    )
    project_version_id = serializers.IntegerField(
        help_text=_("Bundled project version ID, if it exists, it will be bundled"),
        default=0,
    )
    language = serializers.CharField(
        help_text=_("Agent language currently included in the project")
    )
    is_audit = serializers.IntegerField(help_text=_("Agent audit status"))

    class Meta:
        model = IastAgent
        fields = [
            "id",
            "token",
            "version",
            "latest_time",
            "is_running",
            "is_core_running",
            "control",
            "is_control",
            "bind_project_id",
            "project_name",
            "online",
            "project_version_id",
            "language",
            "is_audit",
        ]


class _AgentResponseDataSerializer(serializers.Serializer):
    agent = _AgentResponseDataAgentSerializer()


_ResponseSerializer = get_response_serializer(
    data_serializer=_AgentResponseDataSerializer(),
)


class Agent(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Agent")],
        summary=_("Agent Detail"),
        description=_(
            "Delete the specified project version according to the conditions."
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request, id_):
        try:
            a = int(id_) > 0
            if not a:
                return R.failure(msg=_("Can't find relevant data"))
        except BaseException:
            return R.failure(msg=_("Can't find relevant data"))
        agent = IastAgent.objects.filter(pk=id_).first()
        if agent:
            return R.success(data={"agent": model_to_dict(agent)})
        return R.failure(msg=_("Can't find relevant data"))
