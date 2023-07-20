#!/usr/bin/env python
# datetime:2020/8/4 16:47
import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.engine_heartbeat import IastEngineHeartbeat

logger = logging.getLogger("dongtai.openapi")


class EngineHeartBeatEndPoint(OpenApiEndPoint):
    authentication_classes = ()
    permission_classes = ()
    name = "api-v1-report-upload"
    description = "agent上传报告"

    @extend_schema(
        summary="Agent 上传报告",
        tags=["Agent"],
    )
    def post(self, request):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        logger.info("开始处理心跳数据")
        try:
            client_ip = self.get_client_ip(request)
            data = request.data
            IastEngineHeartbeat.objects.create(
                client_ip=client_ip,
                status=data["status"],
                msg=data["msg"],
                agentcount=data["agentCount"],
                reqcount=data["reqCount"],
                agentenablecount=data["agentEnableCount"],
                projectcount=data["projectCount"],
                usercount=data["userCount"],
                vulcount=data["vulCount"],
                methodpoolcount=data["methodPoolCount"],
                timestamp=data["timestamp"],
            )
            logger.info(_("[{}] Heartbeat data is successful").format(client_ip))
            return R.success(data=data)
        except Exception as e:
            logger.error(_("Heartbeat data failed, error reason: {}").format(e))
            return R.failure()

    @staticmethod
    def get_client_ip(request):
        try:
            logger.info(request.META)
            if "HTTP_X_FORWARDED_FOR" in request.META:
                ip = request.META["HTTP_X_FORWARDED_FOR"]
            else:
                ip = request.META["REMOTE_ADDR"]
            return ip
        except Exception as e:
            logger.error(_("Client IP acquisition failed, reasons: {}").format(e))
            return ""
