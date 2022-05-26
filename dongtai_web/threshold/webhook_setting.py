#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent webHook setting
import time

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.agent_webhook_setting import IastAgentUploadTypeUrl
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.agent_config import AgentWebHookSettingSerializer
from rest_framework.serializers import ValidationError

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('The setting is complete')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class AgentWebHookConfig(UserEndPoint):
    name = "api-v1-agent-webHook-config-setting"
    description = _("config webHook Agent")

    def create_webHook_config(self, user, type_id, url, headers, id):
        try:
            setting = {}
            if id is not None:
                setting = IastAgentUploadTypeUrl.objects.filter(user=user, id=id).first()
            if setting:
                setting.type_id = type_id
                setting.url = url
                setting.headers = headers
            else:
                timestamp = int(time.time())
                setting = IastAgentUploadTypeUrl(
                    user=user,
                    type_id=type_id,
                    url=url,
                    headers=headers,
                    create_time=timestamp
                )
            setting.save()
            return setting
        except Exception as e:
            return None

    @extend_schema_with_envcheck(
        tags=[_('Agent')],
        summary=_('Agent webHook Config'),
        description=_("Agent traffic reporting data forwarding address configuration"),
        response_schema=_ResponseSerializer)
    def post(self, request):
        ser = AgentWebHookSettingSerializer(data=request.data)
        user = request.user
        if ser.is_valid(False):
            id = ser.validated_data.get('id', None)
            type_id = ser.validated_data.get('type_id', None)
            headers = ser.validated_data.get('headers', {})
            url = ser.validated_data.get('url', "").strip()
        else:
            return R.failure(msg=_('Incomplete parameter, please check again'))
        config = self.create_webHook_config(user, type_id, url, headers, id)
        if config:
            return R.success(msg=_('Config has been created successfully'),data={"id":config.id})
        else:
            R.failure(msg=_('Failed to create config'))
