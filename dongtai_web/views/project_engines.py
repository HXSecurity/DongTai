#!/usr/bin/env python

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_common.utils import const
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _ProjectEnginesDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of the agent"))
    token = serializers.CharField(help_text=_("The name of agent"))
    shortname = serializers.CharField(help_text=_("The short name of the agent"))

    class Meta:
        model = IastAgent
        fields = ["id", "name"]


_ProjectEnginesResponseSerializer = get_response_serializer(_ProjectEnginesDataSerializer(many=True))


class ProjectEngines(UserEndPoint):
    name = "api-v1-project-engines"
    description = _("View engine list")

    @extend_schema_with_envcheck(
        tags=[_("Project")],
        summary=_("Projects Agents"),
        description=_("Get the agent list corresponding to the project id."),
        response_schema=_ProjectEnginesResponseSerializer,
    )
    def get(self, request, pid):
        department = request.user.get_relative_department()
        queryset = IastAgent.objects.filter(
            department__in=department,
            online=const.RUNNING,
            bind_project_id__in=[0, pid],
        ).values("id", "token", "alias")
        data = []
        if queryset:
            data = [
                {
                    "id": item["id"],
                    "token": item["token"],
                    "short_name": item["alias"] if item.get("alias", None) else "-".join(item["token"].split("-")[:-1]),
                }
                for item in queryset
            ]

        return R.success(data=data)
