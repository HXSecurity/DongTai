#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/4 16:47
# software: PyCharm
# project: webapi
import logging

from dongtai.models.engine_heartbeat import IastEngineHeartbeat

from dongtai.endpoint import OpenApiEndPoint, R

logger = logging.getLogger("dongtai.openapi")


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
        logger.info('开始处理心跳数据')
        try:
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
            logger.info(f'【{client_ip}】心跳数据处理成功')
            return R.success(data=data)
        except Exception as e:
            logger.error(f'心跳数据处理失败，错误原因：{e}')
            return R.failure()

    @staticmethod
    def get_client_ip(request):
        try:
            logger.info(request.META)
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            return ip
        except Exception as e:
            logger.error(f'客户端IP获取失败，原因：{e}')
            return ''
