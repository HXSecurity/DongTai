#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
import time
from dongtai_common.endpoint import UserEndPoint, R

from dongtai_common.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.agent import AgentToggleArgsSerializer
from dongtai_web.views import AGENT_STATUS
from collections import defaultdict
from dongtai_common.utils.const import OPERATE_PUT

STATUS_MAPPING = defaultdict(lambda: 1, {3: 1, 4: 2})


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
        tags=[
            _('Agent'),
            OPERATE_PUT,
        ],
        deprecated=True,
        summary=_('Agent Status Update'),
        description=_("Control the running agent by specifying the id."),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        ser = AgentCoreStatusSerializer(data=request.data)
        if ser.is_valid(False):
            agent_id = ser.validated_data.get('id', None)
            core_status = ser.validated_data.get('core_status', None)
            agent_ids = ser.validated_data.get('agent_ids', "").strip()
        else:
            return R.failure(msg=_('Incomplete parameter, please check again'))

        if agent_ids:
            try:
                agent_ids = [int(i) for i in agent_ids.split(',')]
            except BaseException:
                return R.failure(_("Parameter error"))
        elif agent_id is not None:
            agent_ids = [int(agent_id)]

        if agent_ids:
            department = request.user.get_relative_department()
            except_running_status = STATUS_MAPPING[core_status]
            # Here could be simply to such as "control_status in statusData.keys()"
            statusData = AGENT_STATUS.get(core_status, {})
            control_status = statusData.get("value", None)
            if control_status is None:
                return R.failure(msg=_('Incomplete parameter, please check again'))

            queryset = IastAgent.objects.filter(department__in=department)
            queryset.filter(id__in=agent_ids).update(
                except_running_status=except_running_status,
                control=core_status,
                is_control=1,
                latest_time=int(time.time()))
            # for agent_id in agent_ids:
            #     agent = IastAgent.objects.filter(user=request.user, id=agent_id).first()
            #     if agent is None:
            #         continue
            #     # edit by song
            #     # if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
            #     #     continue
            #     agent.control = core_status
            #     agent.is_control = 1
            #     agent.latest_time = int(time.time())
            #     agent.save(update_fields=['latest_time', 'control', 'is_control'])

        return R.success(msg=_('状态已下发'))


class AgentCoreStatusUpdateALL(UserEndPoint):
    name = "api-v1-agent-core-status-update"
    description = _("Suspend Agent")

    @extend_schema_with_envcheck(
        request=AgentToggleArgsSerializer,
        tags=[
            _('Agent'),
            OPERATE_PUT,
        ],
        deprecated=True,
        summary="Agent 批量更新",
        description=_("Control the running agent by specifying the id."),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        ser = AgentCoreStatusSerializer(data=request.data)
        department = request.user.get_relative_department()
        if ser.is_valid(False):
            core_status = ser.validated_data.get('core_status', None)
        else:
            return R.failure(msg=_('Incomplete parameter, please check again'))

        #queryset = IastAgent.objects.filter(department__in=department)
        #except_running_status = STATUS_MAPPING[core_status]
        #queryset.filter(online=1).update(
        #    except_running_status=except_running_status,
        #    control=core_status,
        #    is_control=1,
        #    latest_time=int(time.time()))
        return R.success(msg=_('状态已下发'))
