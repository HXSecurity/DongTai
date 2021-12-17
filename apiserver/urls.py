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
from apiserver.views.engine_heartbeat import EngineHeartBeatEndPoint
from apiserver.views.engine_status import EngineUpdateEndPoint
from apiserver.views.engine_status import EngineAction
from apiserver.views.hook_profiles import HookProfilesEndPoint
from apiserver.views.properties import PropertiesEndPoint
from apiserver.views.report_upload import ReportUploadEndPoint
from apiserver.views.health import HealthView
from apiserver.views.health_oss import OSSHealthView
from apiserver.views.agent_limit import LimitView
from apiserver.views.startuptime import (StartupTimeEndPoint,
                                         StartupTimeGzipEndPoint)

urlpatterns = [
    path('agent/download', AgentDownload.as_view()),
    path('agent/limit', LimitView.as_view()),
    path('agent/startuptime', StartupTimeEndPoint.as_view()),
    path('agent/gzipstartuptime', StartupTimeGzipEndPoint.as_view()),
    path('deploy/auto', AutoDeployEndPoint.as_view()),
    path('engine/heartbeat', EngineHeartBeatEndPoint.as_view()),
    path('engine/download', EngineDownloadEndPoint.as_view()),
    path('agent/register', AgentRegisterEndPoint.as_view()),
    path('engine/update', EngineUpdateEndPoint.as_view()),
    path('engine/update/<int:status>', EngineUpdateEndPoint.as_view()),
    path('profiles', HookProfilesEndPoint.as_view()),
    path('properties', PropertiesEndPoint.as_view()),
    path('report/upload', ReportUploadEndPoint.as_view()),
    path('engine/action', EngineAction.as_view()),
    # todo 增加重放请求获取接口，用于后续逻辑漏洞/漏洞验证等功能，暂时先不实现
    path('health', HealthView.as_view()),
    path('oss/health', OSSHealthView.as_view()),
]
