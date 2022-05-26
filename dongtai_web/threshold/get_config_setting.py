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
        configData = IastAgentConfig.objects.filter(user=user)
        result = []
        if configData:
            for item in configData:
                data = model_to_dict(item)
                data_detail = {}
                if data['details']:
                    data_detail = data['details']
                del data['user']
                del data['details']

                if type(data_detail) == dict:

                    data['enableAutoFallback'] = data_detail.get("enableAutoFallback", None)
                    data['hookLimitTokenPerSecond'] = data_detail.get("hookLimitTokenPerSecond", None)
                    data['heavyTrafficLimitTokenPerSecond'] = data_detail.get("heavyTrafficLimitTokenPerSecond", None)
                    data['cpuUsagePercentage'] = data_detail.get("performanceLimitMaxThreshold", {}).get("cpuUsage", {}).get("cpuUsagePercentage",None)
                    data['memUsagePercentage'] = data_detail.get("performanceLimitMaxThreshold", {}).get("memoryUsage", {}).get("memUsagePercentage",None)
                else:
                    data['enableAutoFallback'] = ""
                    data['hookLimitTokenPerSecond'] = ""
                    data['heavyTrafficLimitTokenPerSecond'] = ""
                    data['cpuUsagePercentage'] = ""
                    data['memUsagePercentage'] = ""
                result.append(data)
        else:
            result = []
        return R.success(msg=_('Successfully'), data={"result": result})
