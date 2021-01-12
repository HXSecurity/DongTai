#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:45
# software: PyCharm
# project: lingzhi-agent-server
from django.http import JsonResponse

from apiserver.base.openapi import OpenApiEndPoint
from apiserver.decrypter import parse_data
from apiserver.report.handler.report_handler_factory import ReportHandlerFactory


class ReportUploadView(OpenApiEndPoint):
    name = "iast_report_upload_api"
    description = "IAST-接收检测引擎上传的报告"

    def post(self, request):
        try:
            report = parse_data(request.read())
            report_type = report.get('type')
            handler = ReportHandlerFactory.get_handler(report_type)
            handler.handle(report, request.user)

            return JsonResponse({
                "status": 201,
                "msg": "report upload success."
            })
        except Exception as e:
            return JsonResponse({
                "status": 202,
                "msg": f"report upload failed, reason: {e}"
            })
