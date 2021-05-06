#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/4 16:47
# software: PyCharm
# project: webapi
import logging

from AgentServer.base import R
from apiserver.base.openapi import OpenApiEndPoint
from apiserver.models.engine_heartbeat import IastEngineHeartbeat

logger = logging.getLogger("django")


class EngineHeartBeatEndPoint(OpenApiEndPoint):
    authentication_classes = ()
    permission_classes = ()
    name = "api-v1-report-upload"
    description = "agent上传报告"

    def post(self, request):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        client_ip = self.get_client_ip(request)
        data = request.data
        IastEngineHeartbeat.objects.create(
            client_ip=client_ip,
            status=data['status'],
            msg=data['msg'],
            agentcount=data['agentCount'],
            reqcount=data['reqCount'],
            agentenablecount=data['agentEnableCount'],
            projectcount=data['projectCount'],
            usercount=data['userCount'],
            vulcount=data['vulCount'],
            methodpoolcount=data['methodPoolCount'],
            timestamp=data['timestamp'],
        )
        return R.success(data=data)

    @staticmethod
    def get_client_ip(request):
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip
