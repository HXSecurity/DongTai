#!/usr/bin/env python
# datetime:2021/1/12 下午7:45

import logging

from drf_spectacular.utils import extend_schema
from rest_framework.throttling import SimpleRateThrottle

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_conf.settings import REPORT_UPLOAD_THROTTLE
from dongtai_protocol.decrypter import parse_data
from dongtai_protocol.report.report_handler_factory import ReportHandler

logger = logging.getLogger("dongtai.openapi")


class CustomRateThrottle(SimpleRateThrottle):
    scope = "report_upload"
    rate = REPORT_UPLOAD_THROTTLE

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class ReportUploadEndPoint(OpenApiEndPoint):
    name = "api-v1-report-upload"
    description = "agent上传报告"

    if REPORT_UPLOAD_THROTTLE:
        throttle_classes = [CustomRateThrottle]

    @extend_schema(
        summary="Agent 上传报告",
        tags=["Agent服务端交互协议"],
    )
    def post(self, request):
        try:
            report = parse_data(request.read())
            data = ReportHandler.handler(report, request.user)
            return R.success(msg="report upload success.", data=data)
        except Exception as e:
            logger.exception("report upload failed, reason: ", exc_info=e)
            return R.failure(msg="report upload failed")
