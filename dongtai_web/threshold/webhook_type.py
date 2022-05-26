#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent webHook setting
import time

from dongtai_common.endpoint import UserEndPoint, R

from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('The type is return')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class AgentWebHookTypeList(UserEndPoint):
    name = "api-v1-agent-webHook-type-list"
    description = _("get webhook all type ")

    @extend_schema_with_envcheck(
        tags=[_('WebHook')],
        summary=_('Agent webHook type'),
        description=_("type list of agent webHook"),
        response_schema=_ResponseSerializer)
    def get(self, request):
        typeData = [
            {
                "key": "错误日志",
                "value": 81
            }, {
                "key": "心跳",
                "value": 1
            }, {
                "key": "低风险漏洞",
                "value": 33
            }, {
                "key": "调用链",
                "value": 36
            }, {
                "key": "SCA",
                "value": 17
            }, {
                "key": "SCA批量",
                "value": 18
            }, {
                "key": "ApiSiteMap",
                "value": 97
            },  {
               "key": "硬编码",
               "value": 37
            },  {
               "key": "高频hook限流",
               "value": 65
            }, {
               "key": "高频请求限流",
               "value": 66
            }, {
                "key": "性能监控降级",
                "value": 67
            }, {
                "key": "异常降级",
                "value": 68
            }, {
                "key": "监控线程异常",
                "value": 69
            }, {
                "key": "触发二次降级",
                "value": 70
            }
        ]

        return R.success(msg=_('Get type list successfully'), data={"result": typeData})
