#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
import time
from dongtai.endpoint import UserEndPoint, R

from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from iast.serializers.agent import AgentToggleArgsSerializer 
from iast.views import AGENT_STATUS

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(((201, _('Suspending ...')), ''), ))


class AgentCoreStatusSerializer(serializers.Serializer):

    id = serializers.IntegerField(help_text=_('The id of the webHook.'), required=False)
    core_status = serializers.IntegerField(help_text=_('The type of the webHook.'), required=True)
    agent_ids = serializers.CharField(help_text=_('The cluster_name of the agent.'), max_length=255, required=False)


class AgentCoreStatusUpdate(UserEndPoint):
    name = "api-v1-agent-core-status-update"
    description = _("Suspend Agent")

    @extend_schema_with_envcheck(
        request=AgentToggleArgsSerializer,
        tags=[_('Agent')],
        summary=_('Agent Status Update'),
        description=_("Control the running agent by specifying the id."  ),
        response_schema=_ResponseSerializer)
    def post(self, request):
        print(request.data)
        ser = AgentCoreStatusSerializer(data=request.data)
        if ser.is_valid(False):
            agent_id = ser.validated_data.get('id', None)
            core_status = ser.validated_data.get('core_status', None)
            agent_ids = ser.validated_data.get('ids', "").strip()
        else:
            return R.failure(msg=_('Incomplete parameter, please check again'))

        if agent_ids:
            try:
                agent_ids = [int(i) for i in agent_ids.split(',')]
            except:
                return R.failure(_("Parameter error"))
        elif agent_id is not None:
            agent_ids = [int(agent_id)]

        if agent_ids:
            statusData = AGENT_STATUS.get(core_status,{})
            control_status = statusData.get("value",None)
            if control_status is None:
                return R.failure(msg=_('Incomplete parameter, please check again'))

            for agent_id in agent_ids:
                agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
                if agent is None:
                    continue
                if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
                    continue
                agent.control = core_status
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save(update_fields=['latest_time', 'control', 'is_control'])

        return R.success(msg=_('Suspending ...'))
