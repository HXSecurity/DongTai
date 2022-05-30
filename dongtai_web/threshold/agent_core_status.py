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
            except:
                return R.failure(_("Parameter error"))
        elif agent_id is not None:
            agent_ids = [int(agent_id)]

        if agent_ids:
            statusData = AGENT_STATUS.get(core_status,{})
            control_status = statusData.get("value",None)
            if control_status is None:
                return R.failure(msg=_('Incomplete parameter, please check again'))
            user = request.user

            # 超级管理员
            if user.is_system_admin():
                queryset = IastAgent.objects.all()
            # 租户管理员
            elif user.is_superuser == 2:
                users = self.get_auth_users(user)
                user_ids = list(users.values_list('id', flat=True))
                queryset = IastAgent.objects.filter(user_id__in=user_ids)
            else:
                # 普通用户
                queryset = IastAgent.objects.filter(user=user)
            queryset.filter(id__in=agent_ids).update(control=core_status, is_control=1, latest_time=int(time.time()))
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

    def post(self, request):
        ser = AgentCoreStatusSerializer(data=request.data)
        if ser.is_valid(False):
            core_status = ser.validated_data.get('core_status', None)
        else:
            return R.failure(msg=_('Incomplete parameter, please check again'))
        user = request.user
        # 超级管理员
        if user.is_system_admin():
            queryset = IastAgent.objects.all()
        # 租户管理员
        elif user.is_superuser == 2:
            users = self.get_auth_users(user)
            user_ids = list(users.values_list('id', flat=True))
            queryset = IastAgent.objects.filter(user_id__in=user_ids)
        else:
            # 普通用户
            queryset = IastAgent.objects.filter(user=user)
        queryset.filter(online=1).update(control=core_status,
                                         is_control=1,
                                         latest_time=int(time.time()))
        return R.success(msg=_('状态已下发'))
