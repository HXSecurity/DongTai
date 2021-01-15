#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午6:59
# software: PyCharm
# project: lingzhi-agent-server

# 报告接口：上传报告
from django.urls import path

from apiserver.views.agent_download import AgentDownload
from apiserver.views.agent_register import AgentRegisterEndPoint
from apiserver.views.engine_auto_deploy import AutoDeployEndPoint
from apiserver.views.engine_download import EngineDownloadEndPoint
from apiserver.views.engine_status import EngineUpdateEndPoint
from apiserver.views.hook_profiles import HookProfilesEndPoint
from apiserver.views.properties import PropertiesEndPoint
from apiserver.views.report_upload import ReportUploadEndPoint

urlpatterns = [
    path('agent/download', AgentDownload.as_view()),
    path('deploy/auto', AutoDeployEndPoint.as_view()),

    path('engine/download', EngineDownloadEndPoint.as_view()),
    path('agent/register', AgentRegisterEndPoint.as_view()),
    path('engine/update', EngineUpdateEndPoint.as_view()),
    path('engine/update/<int:status>', EngineUpdateEndPoint.as_view()),
    path('profiles', HookProfilesEndPoint.as_view()),
    path('properties', PropertiesEndPoint.as_view()),
    path('report/upload', ReportUploadEndPoint.as_view()),
    # todo 增加重放请求获取接口，用于后续逻辑漏洞/漏洞验证等功能，暂时先不实现
]
