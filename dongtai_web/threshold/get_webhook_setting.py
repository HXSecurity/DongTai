#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent threshold setting
import time

from django.forms import model_to_dict
from dongtai_common.endpoint import UserEndPoint, R

from dongtai_common.models.agent_webhook_setting import IastAgentUploadTypeUrl

from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Get success')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class GetAgentWebHookConfig(UserEndPoint):
    name = "api-v1-agent-webHook-config-get"
    description = _("config Agent")

    @extend_schema_with_envcheck(
        tags=[_('WebHook')],
        summary=_('WebHook threshold Config get'),
        description=_("WebHook threshold list"),
        response_schema=_ResponseSerializer)
    def get(self, request):
        user = request.user
        configData = IastAgentUploadTypeUrl.objects.filter(user=user).order_by("-create_time")
        data = []
        if configData:
            for item in configData:
                itemData = model_to_dict(item)
                del itemData['user']
                data.append(itemData)

        return R.success(msg=_('Successfully'), data={"result": data})
