#!/usr/bin/env python
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _UserAgentResponseDataSerializer(serializers.Serializer):
    token = serializers.CharField(help_text=_("The name of agent"))
    id = serializers.CharField(help_text=_("The id of agent"))


_AgentResponseSerializer = get_response_serializer(
    data_serializer=_UserAgentResponseDataSerializer(many=True),
)


class UserAgentList(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Agent")],
        summary=_("Agent (with user)"),
        description=_("Stop the running agent by specifying the id."),
        response_schema=_AgentResponseSerializer,
    )
    def get(self, request):
        user = request.user
        queryset = (
            IastAgent.objects.all()
            if user.is_talent_admin()
            else IastAgent.objects.filter(user=user)
        )
        queryset_datas = queryset.values("id", "token")
        data = []
        if queryset_datas:
            for item in queryset_datas:
                data.append({"id": item["id"], "name": item["token"]})
        return R.success(data=data)
