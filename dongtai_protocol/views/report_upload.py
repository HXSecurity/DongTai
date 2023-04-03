#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:45
# software: PyCharm
# project: lingzhi-agent-server

from dongtai_common.endpoint import OpenApiEndPoint, R
from drf_spectacular.utils import extend_schema
import time
import logging
from dongtai_protocol.api_schema import DongTaiParameter
from dongtai_protocol.decrypter import parse_data
from dongtai_protocol.report.report_handler_factory import ReportHandler
from rest_framework.views import APIView
from django.http import JsonResponse

logger = logging.getLogger('dongtai.openapi')


class ReportUploadEndPoint(OpenApiEndPoint):
    name = "api-v1-report-upload"
    description = "agent上传报告"

    @extend_schema(
        description='Pull Agent Engine Hook Rule',
        parameters=[
            DongTaiParameter.LANGUAGE,
        ],
        responses=R,
        methods=['GET']
    )
    def post(self, request):
        try:
            report = parse_data(request.read())
            data = ReportHandler.handler(report, request.user)
            return R.success(msg="report upload success.", data=data)
        except Exception as e:
            logger.error(f"report upload failed, reason: {e}", exc_info=e)
            return R.failure(msg="report upload failed")
