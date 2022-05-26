#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent threshold setting
import time

from django.forms import model_to_dict
from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.agent_config import IastAgentConfig
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Get detail success')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class GetAgentThresholdConfigDetail(UserEndPoint):
    name = "api-v1-agent-threshold-config-get-detail"
    description = _("config Agent")

    @extend_schema_with_envcheck(
        tags=[_('Agent')],
        summary=_('Agent threshold Config'),
        description=_("Configure agent disaster recovery strategy"),
        response_schema=_ResponseSerializer)
    def get(self, request, pk):
        user = request.user
        configData = IastAgentConfig.objects.filter(user=user, pk=pk).first()
        result = {}
        if configData:
            result = model_to_dict(configData)

        return R.success(msg=_('Successfully'), data={"result": result})
