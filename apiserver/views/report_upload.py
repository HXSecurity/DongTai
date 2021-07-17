#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:45
# software: PyCharm
# project: lingzhi-agent-server

from AgentServer.base import R
from apiserver.base.openapi import OpenApiEndPoint
from apiserver.decrypter import parse_data
from apiserver.report.report_handler_factory import ReportHandler


class ReportUploadEndPoint(OpenApiEndPoint):
    name = "api-v1-report-upload"
    description = "agent上传报告"

    def post(self, request):
        try:
            report = parse_data(request.read())
            data = ReportHandler.handler(report, request.user)

            return R.success(msg="report upload success.", data=data)
        except Exception as e:
            return R.failure(msg=f"report upload failed, reason: {e}")
