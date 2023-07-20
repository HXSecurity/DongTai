#!/usr/bin/env python
# datetime:2021/1/12 下午7:45

import logging
import time

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_protocol.api_schema import DongTaiParameter
from dongtai_protocol.decrypter import parse_data
from dongtai_protocol.report.report_handler_factory import ReportHandler

logger = logging.getLogger("dongtai.openapi")


class ReportUploadEndPoint(OpenApiEndPoint):
    name = "api-v1-report-upload"
    description = "agent上传报告"

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
            logger.error(f"report upload failed, reason: {e}", exc_info=e)
            return R.failure(msg="report upload failed")
