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
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from iast.serializers.agent_config import AgentConfigSettingSerializer
from rest_framework.serializers import ValidationError

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('The setting is complete')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class AgentThresholdConfig(UserEndPoint):
    name = "api-v1-agent-threshold-config-setting"
    description = _("config Agent")

    def create_agent_config(self,user, details, hostname, ip, port, cluster_name, cluster_version, priority,id):
        try:

            timestamp = int(time.time())
            if id:
                strategy = IastAgentConfig.objects.filter(user=user,id=id).order_by("-create_time").first()
            else:
                strategy = IastAgentConfig.objects.filter(user=user, id=id).order_by("-create_time").first()
            if strategy:
                strategy.details = details
                strategy.hostname = hostname
                strategy.ip = ip
                strategy.port = port
                strategy.cluster_name = cluster_name
                strategy.cluster_version = cluster_version
                strategy.priority = priority
            else:
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
        tags=[_('Agent')],
        summary=_('Agent threshold Config'),
        description=_("Configure agent disaster recovery strategy"),
        response_schema=_ResponseSerializer)
    def post(self, request):

        ser = AgentConfigSettingSerializer(data=request.data)
        user = request.user
        try:
            if ser.is_valid(True):
                details = ser.validated_data.get('details', {})
                hostname = ser.validated_data.get('hostname', "").strip()
                ip = ser.validated_data.get('ip', "")
                id = ser.validated_data.get('id', "")
                port = ser.validated_data.get('port', 80)
                cluster_name = ser.validated_data.get('cluster_name', "").strip()
                cluster_version = ser.validated_data.get('cluster_version', "")
                priority = ser.validated_data.get('priority', 0)

        except ValidationError as e:

            return R.failure(data=e.detail)

        config = self.create_agent_config(user, details, hostname, ip, port, cluster_name, cluster_version, priority,id)
        if config:
            return R.success(msg=_('保存成功'))
        else:
            return R.failure(msg=_('保存失败'))
