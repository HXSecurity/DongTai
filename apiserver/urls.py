#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午6:59
# software: PyCharm
# project: lingzhi-agent-server

# 报告接口：上传报告
from django.urls import path

from apiserver.views.agent_register import AgentRegisterEndPoint
from apiserver.views.engine_auto_deploy import AutoDeployEndPoint
from apiserver.views.engine_download import EngineDownloadEndPoint
from apiserver.views.engine_status import EngineUpdateEndPoint
from apiserver.views.hook_profile_init import HookProfileInitEndPoint
from apiserver.views.hook_profiles import HookProfilesEndPoint
from apiserver.views.properties import PropertiesEndPoint
from apiserver.views.report_upload import ReportUploadEndPoint

urlpatterns = [
    path('report/upload', ReportUploadEndPoint.as_view()),
    # fixme 后续api接口地址统一调整为agent/register
    path('agent/register', AgentRegisterEndPoint.as_view()),
    # todo 增加hook策略下载接口
    path('deploy/auto', AutoDeployEndPoint.as_view()),
    # todo 增加
    path('engine/download', EngineDownloadEndPoint.as_view()),
    path('engine/status', EngineUpdateEndPoint.as_view()),
    path('profiles', HookProfilesEndPoint.as_view()),
    path('properties', PropertiesEndPoint.as_view()),
    # path('profile/init', HookProfileInitEndPoint.as_view()),
]
