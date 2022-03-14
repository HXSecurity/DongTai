#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent threshold setting
import time

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.agent_config import IastAgentConfig
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from iast.serializers.agent_config import AgentConfigSettingSerializer


_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('The installation is complete')), ''),
    ((202, _('The engine is being installed or uninstalled, please try again later')), ''),
    ((202, _('Engine does not exist or no permission to access')),
     ''),
))


class AgentThresholdConfig(UserEndPoint):
    name = "api-v1-agent-threshold-config-setting"
    description = _("config Agent")

    def parse_args(self, request):
        """
        :param request:
        :return:
        """
        try:
            details = request.data.get('details')
            hostname = request.data.get('hostname').strip()
            ip = request.data.get('ip').strip()
            port = request.data.get('port')
            cluster_name = request.data.get('cluster_name').strip()
            cluster_version = request.data.get('cluster_version')
            priority = request.data.get('priority')
            return details, hostname, ip, port, cluster_name, cluster_version, priority
        except Exception as e:
            return None, None, None, None, None, None, None

    def create_agent_config(self,user, details, hostname, ip, port, cluster_name, cluster_version, priority):
        try:

            timestamp = int(time.time())
            strategy = IastAgentConfig(
                user=user,
                details=details,
                hostname=hostname,
                ip=ip,
                port=port,
                cluster_name=cluster_name,
                cluster_version=cluster_version,
                priority=priority,
                create_time=timestamp
            )
            strategy.save()
            return strategy
        except Exception as e:
            return None

    @extend_schema_with_envcheck(
        request=AgentConfigSettingSerializer,
        tags=[_('Agent')],
        summary=_('Agent Config'),
        description=_("Install the running agent by specifying the id."),
        response_schema=_ResponseSerializer)
    def post(self, request):
        user = request.user
        details, hostname, ip, port, cluster_name, cluster_version, priority = self.parse_args(request)
        if all((details, hostname, ip, port, cluster_name, cluster_version, priority)) is False:
            return R.failure(msg=_('Incomplete parameter, please check again'))
        config = self.create_agent_config(user, details, hostname, ip, port, cluster_name, cluster_version, priority)
        if config:
            return R.success(msg=_('Config has been created successfully'))
        else:
            R.failure(msg=_('Failed to create config'))
