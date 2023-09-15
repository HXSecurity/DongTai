import json
from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.profile import IastProfile
from dongtai_conf.patch import patch_point, to_patch
from dongtai_web.utils import extend_schema_with_envcheck


class _AgentConfigArgsSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField(required=True, help_text=_("Agent id"))


REPORT_VALIDATED_SINK_KEY = "report_validated_sink"
DEFAULT_REPORT_VALIDATED_SINK = {"report_validated_sink": False}


def get_report_validated_sink_profile() -> dict[str, bool]:
    profile = IastProfile.objects.filter(key=REPORT_VALIDATED_SINK_KEY).values_list("value", flat=True).first()
    if profile is None:
        IastProfile(
            key=REPORT_VALIDATED_SINK_KEY,
            value=json.dumps(DEFAULT_REPORT_VALIDATED_SINK),
        ).save()
        return DEFAULT_REPORT_VALIDATED_SINK
    return json.loads(profile)


class AgentConfigAllinOneView(OpenApiEndPoint):
    @extend_schema_with_envcheck(
        [_AgentConfigArgsSerializer],
        summary="agent配置",
        tags=["Agent服务端交互协议"],
        methods=["GET"],
    )
    @to_patch
    def get(self, request):
        ser = _AgentConfigArgsSerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError as e:
            return R.failure(data=e.detail)
        agent_id: int = ser.data["agent_id"]
        agent = IastAgent.objects.filter(pk=agent_id).first()
        if not agent:
            return R.failure(msg="No agent found.")
        data: dict[str, Any] = {}
        data, agent_id = patch_point(data, agent_id)
        if agent.bind_project is not None and agent.bind_project.enable_log is not None:
            data["enable_log"] = agent.bind_project.enable_log
        if agent.bind_project is not None and agent.bind_project.log_level is not None:
            data["log_level"] = agent.bind_project.log_level
        data[REPORT_VALIDATED_SINK_KEY] = get_report_validated_sink_profile()[REPORT_VALIDATED_SINK_KEY]
        return R.success(data=data)
