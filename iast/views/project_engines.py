#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _

from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers


class _ProjectEnginesDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of the agent"))
    token = serializers.CharField(help_text=_('The name of agent'))
    shortname = serializers.CharField(
        help_text=_("The short name of the agent"))

    class Meta:
        model = IastAgent
        fields = ['id', 'name']


_ProjectEnginesResponseSerializer = get_response_serializer(
    _ProjectEnginesDataSerializer(many=True))


class ProjectEngines(UserEndPoint):
    name = "api-v1-project-engines"
    description = _("View engine list")

    @extend_schema_with_envcheck(
        tags=[_('Project')],
        summary=_('Projects Agents'),
        description=_("Get the agent list corresponding to the project id."),
        response_schema=_ProjectEnginesResponseSerializer,
    )
    def get(self, request, pid):
        auth_users = self.get_auth_users(request.user)
        queryset = IastAgent.objects.filter(
            user__in=auth_users,
            online=const.RUNNING,
            bind_project_id__in=[0, pid]).values("id", "token","alias")
        data = []
        if queryset:
            for item in queryset:
                data.append({
                    'id':
                    item['id'],
                    'token':
                    item['token'],
                    'short_name':
                    item['alias'] if item.get('alias', None) else '-'.join(
                        item['token'].split('-')[:-1]),
                })
        return R.success(data=data)
