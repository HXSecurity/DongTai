#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent threshold setting
import time

from django.forms import model_to_dict
from dongtai.endpoint import UserEndPoint, R
from dongtai.models.agent_config import IastAgentConfig
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Get success')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class GetAgentThresholdConfig(UserEndPoint):
    name = "api-v1-agent-threshold-config-get"
    description = _("config Agent")

    @extend_schema_with_envcheck(
        tags=[_('Agent')],
        summary=_('Agent threshold Config'),
        description=_("Configure agent disaster recovery strategy"),
        response_schema=_ResponseSerializer)
    def get(self, request):
        user = request.user
        configData = IastAgentConfig.objects.filter(user=user).order_by("-create_time").first()
        if configData:
            data = model_to_dict(configData)
            del data['user']
            del data['id']
        else:
            data = {}
        return R.success(msg=_('Successfully'), data=data)
