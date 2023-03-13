#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent webHook setting
import time

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.agent_config import IastAgentConfig
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.agent_config import AgentWebHookDelSerializer
from rest_framework.serializers import ValidationError

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('The setting is complete')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class DelAgentThresholdConfig(UserEndPoint):
    name = "api-v1-agent-Threshold-config-del"
    description = _("del webHook Agent")

    @extend_schema_with_envcheck(
        tags=[_('Agent')],
        summary=_('Agent webHook delete'),
        description=_("Delete agent traffic reporting data forwarding address configuration"),
        response_schema=_ResponseSerializer)
    def post(self, request):
        ser = AgentWebHookDelSerializer(data=request.data)
        user = request.user
        if ser.is_valid(False):
            id = ser.validated_data.get('id', None)
        else:
            return R.failure(msg=_('Incomplete parameter, please check again'))
        config = IastAgentConfig.objects.filter(user=user, id=id).delete()
        if config:
            return R.success(msg=_('Config has been deleted successfully'))
        else:
            R.failure(msg=_('Failed to delete config'))
