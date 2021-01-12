#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午6:59
# software: PyCharm
# project: lingzhi-agent-server

# 报告接口：上传报告
from django.urls import path

from apiserver.views.report_upload import ReportUploadView

urlpatterns = [
    path('report/upload', ReportUploadView.as_view()),
]
